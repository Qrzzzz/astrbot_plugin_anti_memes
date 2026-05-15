from __future__ import annotations

from collections import OrderedDict


def mark_processed(cache: OrderedDict[str, None], key: str, limit: int) -> None:
    cache[key] = None
    cache.move_to_end(key)
    while len(cache) > max(100, int(limit)):
        cache.popitem(last=False)
