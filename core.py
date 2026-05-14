from __future__ import annotations

from collections import OrderedDict
from typing import Any


def is_digits(value: str) -> bool:
    return value.isdigit() and len(value) > 0


def normalize_targets(raw_targets: Any) -> dict[str, list[str]]:
    normalized: dict[str, list[str]] = {}
    if not isinstance(raw_targets, dict):
        return normalized
    for group_id, users in raw_targets.items():
        group_id_str = str(group_id).strip()
        if not is_digits(group_id_str) or not isinstance(users, list):
            continue
        uniq_users: list[str] = []
        for user_id in users:
            user_id_str = str(user_id).strip()
            if is_digits(user_id_str) and user_id_str not in uniq_users:
                uniq_users.append(user_id_str)
        if uniq_users:
            normalized[group_id_str] = uniq_users
    return normalized


def raw_message_has_image(raw_message: Any) -> bool:
    if isinstance(raw_message, str):
        return "[CQ:image" in raw_message
    if isinstance(raw_message, list):
        for node in raw_message:
            if isinstance(node, dict) and str(node.get("type", "")).lower() == "image":
                return True
    return False


def mark_processed(cache: OrderedDict[str, None], message_id: str, limit: int) -> None:
    cache[message_id] = None
    cache.move_to_end(message_id)
    while len(cache) > max(100, int(limit)):
        cache.popitem(last=False)
