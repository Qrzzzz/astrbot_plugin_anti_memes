from __future__ import annotations

from collections import OrderedDict
from typing import Any

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register

from core import is_digits, mark_processed, normalize_targets, raw_message_has_image

PLUGIN_NAME = "astrbot_plugin_anti_memes"
PLUGIN_AUTHOR = "Qrzzzz"
PLUGIN_DESC = "按群号与 QQ 号配置目标用户，自动撤回其发送的图片消息。"
PLUGIN_VERSION = "1.0.0"

USAGE_ADD = "用法：/add_recall <群号> <QQ号>"
USAGE_DEL = "用法：/del_recall <群号> <QQ号>"


@register(PLUGIN_NAME, PLUGIN_AUTHOR, PLUGIN_DESC, PLUGIN_VERSION)
class ImageRecaller(Star):
    """Monitor configured users in configured groups and recall image messages."""

    def __init__(self, context: Context, config: Any | None = None) -> None:
        super().__init__(context)
        self.config = config if config is not None else getattr(self, "config", None)
        self._processed_lock = __import__("asyncio").Lock()
        self.processed_msg_ids: OrderedDict[str, None] = OrderedDict()
        self.targets: dict[str, list[str]] = normalize_targets(self._config_get("targets", {}))

    async def initialize(self) -> None:
        self.targets = normalize_targets(self._config_get("targets", {}))
        logger.info("anti_memes plugin initialized (realtime recall mode).")

    async def terminate(self) -> None:
        logger.info("anti_memes plugin terminated.")

    def _config_get(self, key: str, default: Any) -> Any:
        if self.config is None:
            return default
        if hasattr(self.config, "get"):
            return self.config.get(key, default)
        return default

    def _save_config(self) -> None:
        if self.config is not None and hasattr(self.config, "save_config"):
            self.config.save_config()

    def _set_targets(self, targets: dict[str, list[str]]) -> None:
        self.targets = normalize_targets(targets)
        if self.config is not None and hasattr(self.config, "__setitem__"):
            self.config["targets"] = self.targets
        self._save_config()

    def _has_manage_permission(self, event: AstrMessageEvent) -> bool:
        sender = getattr(getattr(event, "message_obj", None), "sender", None)
        role = str(getattr(sender, "role", "")).lower()
        if role in {"owner", "admin"}:
            return True
        for attr in ("is_admin", "is_superuser"):
            checker = getattr(event, attr, None)
            if callable(checker):
                try:
                    if checker():
                        return True
                except Exception:
                    continue
        return False

    def _message_has_image(self, message_obj: Any) -> bool:
        chain = getattr(message_obj, "message", None)
        if isinstance(chain, list):
            for node in chain:
                node_type = str(getattr(node, "type", "")).lower()
                class_name = node.__class__.__name__.lower()
                if node_type == "image" or class_name == "image":
                    return True
                if isinstance(node, dict) and str(node.get("type", "")).lower() == "image":
                    return True
        return raw_message_has_image(getattr(message_obj, "raw_message", None))

    def _cache_limit(self) -> int:
        value = self._config_get("processed_cache_size", 2000)
        try:
            limit = int(value)
        except (TypeError, ValueError):
            return 2000
        return max(100, limit)

    def _is_processed(self, message_id: str) -> bool:
        return message_id in self.processed_msg_ids

    def _mark_processed(self, message_id: str) -> None:
        mark_processed(self.processed_msg_ids, message_id, self._cache_limit())

    async def _try_recall(
        self, event: AstrMessageEvent, message_id: str, group_id: str, user_id: str
    ) -> bool:
        try:
            await event.bot.api.call_action("delete_msg", message_id=int(message_id))
            logger.info("recall success group=%s user=%s message=%s", group_id, user_id, message_id)
            return True
        except Exception as exc:
            logger.warning(
                "recall failed group=%s user=%s message=%s err=%s",
                group_id,
                user_id,
                message_id,
                exc,
            )
            return False

    @filter.command("add_recall")
    async def add_recall(
        self, event: AstrMessageEvent, group_id: str | None = None, user_id: str | None = None
    ):
        """添加监控目标。用法：/add_recall <群号> <QQ号>"""
        if not self._has_manage_permission(event):
            yield event.plain_result("❌ 权限不足：仅管理员可配置规则。")
            return
        if not group_id or not user_id:
            yield event.plain_result(f"参数错误，{USAGE_ADD}")
            return

        group_id, user_id = group_id.strip(), user_id.strip()
        if not is_digits(group_id) or not is_digits(user_id):
            yield event.plain_result(f"群号和 QQ 号必须为纯数字字符串。{USAGE_ADD}")
            return

        targets = dict(self.targets)
        users = list(targets.get(group_id, []))
        if user_id in users:
            yield event.plain_result("⚠️ 该用户已在监控列表中。")
            return

        users.append(user_id)
        targets[group_id] = users
        self._set_targets(targets)
        yield event.plain_result(f"✅ 已添加监控：群 {group_id} 用户 {user_id}")

    @filter.command("del_recall")
    async def del_recall(
        self, event: AstrMessageEvent, group_id: str | None = None, user_id: str | None = None
    ):
        """删除监控目标。用法：/del_recall <群号> <QQ号>"""
        if not self._has_manage_permission(event):
            yield event.plain_result("❌ 权限不足：仅管理员可配置规则。")
            return
        if not group_id or not user_id:
            yield event.plain_result(f"参数错误，{USAGE_DEL}")
            return

        group_id, user_id = group_id.strip(), user_id.strip()
        if not is_digits(group_id) or not is_digits(user_id):
            yield event.plain_result(f"群号和 QQ 号必须为纯数字字符串。{USAGE_DEL}")
            return

        targets = dict(self.targets)
        users = list(targets.get(group_id, []))
        if user_id not in users:
            yield event.plain_result("⚠️ 未找到该监控规则。")
            return

        users.remove(user_id)
        if users:
            targets[group_id] = users
        else:
            targets.pop(group_id, None)
        self._set_targets(targets)
        yield event.plain_result(f"🗑️ 已移除监控：群 {group_id} 用户 {user_id}")

    @filter.command("list_recall")
    async def list_recall(self, event: AstrMessageEvent):
        """列出全部监控规则。用法：/list_recall"""
        if not self._has_manage_permission(event):
            yield event.plain_result("❌ 权限不足：仅管理员可查看规则。")
            return
        if not self.targets:
            yield event.plain_result("📭 当前监控列表为空。")
            return

        lines = ["🔍 当前监控列表："]
        for group_id in sorted(self.targets.keys()):
            lines.append(f"- 群 {group_id}: {', '.join(self.targets[group_id])}")
        yield event.plain_result("\n".join(lines))

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent) -> None:
        if not self._config_get("enable_realtime_recall", True):
            return
        message_obj = event.message_obj
        group_id = str(getattr(message_obj, "group_id", ""))
        user_id = str(getattr(getattr(message_obj, "sender", None), "user_id", ""))
        message_id = str(getattr(message_obj, "message_id", ""))

        if not (is_digits(group_id) and is_digits(user_id) and is_digits(message_id)):
            return
        if group_id not in self.targets or user_id not in self.targets[group_id]:
            return
        if not self._message_has_image(message_obj):
            return

        async with self._processed_lock:
            if self._is_processed(message_id):
                return
            ok = await self._try_recall(event, message_id, group_id, user_id)
            self._mark_processed(message_id)
            if ok:
                event.stop_event()
