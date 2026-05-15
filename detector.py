from __future__ import annotations

from typing import Any


def raw_message_has_image(raw_message: Any) -> bool:
    if raw_message is None:
        return False
    if isinstance(raw_message, str):
        return "[cq:image" in raw_message.lower()
    if isinstance(raw_message, dict):
        msg_type = str(raw_message.get("type", "")).lower()
        return msg_type == "image"
    if isinstance(raw_message, list):
        for node in raw_message:
            if isinstance(node, dict) and str(node.get("type", "")).lower() == "image":
                return True
    return False


def message_obj_has_image(message_obj: Any) -> bool:
    chain = getattr(message_obj, "message", None)
    if isinstance(chain, list):
        for node in chain:
            if isinstance(node, dict) and str(node.get("type", "")).lower() == "image":
                return True
            node_type = str(getattr(node, "type", "")).lower()
            if node_type == "image" or node.__class__.__name__.lower() == "image":
                return True
    return raw_message_has_image(getattr(message_obj, "raw_message", None))
