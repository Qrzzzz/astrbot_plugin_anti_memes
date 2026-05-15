from __future__ import annotations

from typing import Any


def build_diagnose_text(event: Any, dry_run: bool, cfg_ok: bool, delete_ok: bool) -> str:
    msg_obj = getattr(event, "message_obj", None)
    group_id = str(getattr(msg_obj, "group_id", ""))
    is_group = bool(group_id)
    adapter = str(getattr(getattr(event, "platform_meta", None), "name", "unknown"))
    return (
        f"群聊环境: {'是' if is_group else '否'}\n"
        f"适配器: {adapter}\n"
        f"delete_msg可用: {'是' if delete_ok else '否'}\n"
        f"配置有效: {'是' if cfg_ok else '否'}\n"
        f"dry_run: {'开启' if dry_run else '关闭'}"
    )
