from __future__ import annotations

from collections import OrderedDict
from datetime import datetime, timezone
from typing import Any

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register

from detector import message_obj_has_image
from diagnostics import build_diagnose_text
from models import RuntimeStats
from platform_onebot import delete_msg
from rules import find_rule, is_digits, migrate_targets_to_rules
from storage import mark_processed


@register("astrbot_plugin_anti_memes", "Qrzzzz", "图片精准撤回助手", "1.1.0")
class ImageRecaller(Star):
    def __init__(self, context: Context, config: Any | None = None) -> None:
        super().__init__(context)
        self.config = config if config is not None else getattr(self, "config", None)
        self.rules = []
        self.stats = RuntimeStats()
        self._processed_lock = __import__("asyncio").Lock()
        self.processed_msg_ids: OrderedDict[str, None] = OrderedDict()

    def _cfg(self, k: str, d: Any) -> Any:
        return self.config.get(k, d) if self.config and hasattr(self.config, "get") else d

    def _save(self) -> None:
        if self.config and hasattr(self.config, "save_config"):
            self.config.save_config()

    def _sync_rules_to_config(self) -> None:
        if self.config and hasattr(self.config, "__setitem__"):
            self.config["rules"] = [r.__dict__ for r in self.rules]
        self._save()

    async def initialize(self) -> None:
        conf = {"rules": self._cfg("rules", []), "targets": self._cfg("targets", {})}
        self.rules = migrate_targets_to_rules(conf)

    def _can_manage(self, event: AstrMessageEvent) -> bool:
        sender = getattr(getattr(event, "message_obj", None), "sender", None)
        role = str(getattr(sender, "role", "")).lower()
        return role in {"owner", "admin"} or getattr(event, "is_admin", lambda: False)()

    def _current_group(self, event: AstrMessageEvent) -> str | None:
        gid = str(getattr(getattr(event, "message_obj", None), "group_id", "")).strip()
        return gid if is_digits(gid) else None

    @filter.command_group("am")
    def am(self):
        pass

    @filter.command("help", parent="am", alias={"anti_memes"})
    async def am_help(self, event: AstrMessageEvent):
        yield event.plain_result(
            "/am add [群号] <QQ号|@用户>\n"
            "/am del [群号] <QQ号>\n/am list [群号]\n"
            "/am dryrun on|off\n/am diagnose"
        )

    async def _add_rule(self, gid: str, uid: str) -> str:
        if find_rule(self.rules, gid, uid):
            return "⚠️ 规则已存在"
        self.rules.append(__import__("models").Rule(group_id=gid, user_id=uid))
        self._sync_rules_to_config()
        return "✅ 添加成功"

    @filter.command("add", parent="am")
    async def am_add(self, event: AstrMessageEvent, a: str | None = None, b: str | None = None):
        if not self._can_manage(event):
            yield event.plain_result("❌ 权限不足")
            return
        gid, uid = (a, b) if b else (self._current_group(event), a)
        if uid and uid.startswith("[CQ:at,qq="):
            uid = uid.split("qq=")[-1].rstrip("]")
        if not (gid and uid and is_digits(gid) and is_digits(uid)):
            yield event.plain_result("参数错误")
            return
        yield event.plain_result(await self._add_rule(gid, uid))

    @filter.command("del", parent="am")
    async def am_del(self, event: AstrMessageEvent, a: str | None = None, b: str | None = None):
        if not self._can_manage(event):
            yield event.plain_result("❌ 权限不足")
            return
        gid, uid = (a, b) if b else (self._current_group(event), a)
        if not (gid and uid and is_digits(gid) and is_digits(uid)):
            yield event.plain_result("参数错误")
            return
        r = find_rule(self.rules, gid, uid)
        if not r:
            yield event.plain_result("⚠️ 用户不在规则中")
            return
        self.rules.remove(r)
        self._sync_rules_to_config()
        yield event.plain_result("🗑️ 删除成功")

    @filter.command("list", parent="am")
    async def am_list(self, event: AstrMessageEvent, gid: str | None = None):
        if not self._can_manage(event):
            yield event.plain_result("❌ 权限不足")
            return
        rows = [r for r in self.rules if (not gid or r.group_id == gid)]
        if not rows:
            yield event.plain_result("📭 无规则")
            return
        text = "\n".join(
            [f"{r.group_id}:{r.user_id} [{'on' if r.enabled else 'off'}]" for r in rows[:20]]
        )
        yield event.plain_result(text)

    @filter.command("dryrun", parent="am")
    async def am_dryrun(self, event: AstrMessageEvent, mode: str = "off"):
        if not self._can_manage(event):
            yield event.plain_result("❌ 权限不足")
            return
        self.config["dry_run"] = (mode.lower() == "on")
        self._save()
        yield event.plain_result(f"dry_run={'on' if self._cfg('dry_run', False) else 'off'}")

    @filter.command("diagnose", parent="am")
    async def am_diagnose(self, event: AstrMessageEvent):
        txt = build_diagnose_text(event, self._cfg("dry_run", False), True, True)
        yield event.plain_result(txt)

    @filter.command("add_recall")
    async def add_recall(self, event: AstrMessageEvent, group_id: str, user_id: str):
        async for x in self.am_add(event, group_id, user_id):
            yield x

    @filter.command("del_recall")
    async def del_recall(self, event: AstrMessageEvent, group_id: str, user_id: str):
        async for x in self.am_del(event, group_id, user_id):
            yield x

    @filter.command("list_recall")
    async def list_recall(self, event: AstrMessageEvent):
        async for x in self.am_list(event, None):
            yield x

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent) -> None:
        self.stats.total_seen += 1
        if not self._cfg("enable_realtime_recall", True):
            self.stats.total_skipped += 1
            return
        mo = event.message_obj
        gid = str(getattr(mo, "group_id", ""))
        uid = str(getattr(getattr(mo, "sender", None), "user_id", ""))
        mid = str(getattr(mo, "message_id", ""))
        if not (is_digits(gid) and is_digits(uid) and is_digits(mid)):
            self.stats.total_skipped += 1
            return
        rule = find_rule(self.rules, gid, uid)
        if not rule or not rule.enabled:
            self.stats.total_skipped += 1
            return
        if not message_obj_has_image(mo):
            self.stats.total_skipped += 1
            return
        self.stats.total_matched += 1
        async with self._processed_lock:
            key = f"{gid}:{uid}:{mid}"
            if key in self.processed_msg_ids:
                return
            try:
                if self._cfg("dry_run", False):
                    self.stats.total_skipped += 1
                else:
                    await delete_msg(event, mid)
                    self.stats.total_recalled += 1
                    self.stats.last_recall_time = datetime.now(timezone.utc).isoformat()
                    if self._cfg("stop_event_after_recall", True):
                        event.stop_event()
            except Exception as exc:
                self.stats.total_failed += 1
                self.stats.last_error = str(exc)
                logger.warning("recall failed: %s", exc)
            finally:
                limit = int(self._cfg("processed_cache_size", 2000))
                mark_processed(self.processed_msg_ids, key, limit)
