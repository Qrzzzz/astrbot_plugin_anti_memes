from __future__ import annotations

from typing import Any


async def delete_msg(event: Any, message_id: str) -> None:
    await event.bot.api.call_action("delete_msg", message_id=int(message_id))
