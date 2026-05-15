from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class ActionMode(str, Enum):
    RECALL = "recall"


@dataclass
class Rule:
    group_id: str
    user_id: str
    enabled: bool = True
    match_image: bool = True
    action: str = ActionMode.RECALL.value
    notify_group: bool = False
    notify_admin: bool = False
    cooldown_seconds: int = 0
    note: str = ""

    def key(self) -> str:
        return f"{self.group_id}:{self.user_id}"


@dataclass
class RuntimeStats:
    total_seen: int = 0
    total_matched: int = 0
    total_recalled: int = 0
    total_failed: int = 0
    total_skipped: int = 0
    last_error: str = ""
    last_recall_time: str = ""


@dataclass
class PluginConfig:
    enable_realtime_recall: bool = True
    enable_polling_fallback: bool = False
    poll_interval_seconds: int = 30
    processed_cache_size: int = 2000
    stop_event_after_recall: bool = True
    dry_run: bool = False
    log_level: str = "INFO"
    notify_on_success: bool = False
    notify_on_failure: bool = True
    protect_bot_self: bool = True
    protect_admins: bool = True
    enable_at_parse: bool = True
    max_rules_per_group: int = 100
    rules: list[Rule] = field(default_factory=list)
    targets: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["rules"] = [asdict(r) for r in self.rules]
        return d
