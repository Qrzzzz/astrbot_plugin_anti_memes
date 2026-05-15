from __future__ import annotations

from typing import Any

from models import Rule


def is_digits(value: str) -> bool:
    return isinstance(value, str) and value.isdigit() and len(value) > 0


def normalize_targets(raw_targets: Any) -> dict[str, list[str]]:
    normalized: dict[str, list[str]] = {}
    if not isinstance(raw_targets, dict):
        return normalized
    for group_id, users in raw_targets.items():
        gid = str(group_id).strip()
        if not is_digits(gid) or not isinstance(users, list):
            continue
        uniq: list[str] = []
        for user_id in users:
            uid = str(user_id).strip()
            if is_digits(uid) and uid not in uniq:
                uniq.append(uid)
        if uniq:
            normalized[gid] = uniq
    return normalized


def migrate_targets_to_rules(config: dict[str, Any]) -> list[Rule]:
    rules_data = config.get("rules", [])
    rules: list[Rule] = []
    if isinstance(rules_data, list):
        for item in rules_data:
            if not isinstance(item, dict):
                continue
            gid = str(item.get("group_id", "")).strip()
            uid = str(item.get("user_id", "")).strip()
            if is_digits(gid) and is_digits(uid):
                base = Rule(group_id=gid, user_id=uid).__dict__
                rules.append(Rule(**{**base, **item, "group_id": gid, "user_id": uid}))
    for gid, users in normalize_targets(config.get("targets", {})).items():
        for uid in users:
            if not any(r.group_id == gid and r.user_id == uid for r in rules):
                rules.append(Rule(group_id=gid, user_id=uid))
    return rules


def find_rule(rules: list[Rule], group_id: str, user_id: str) -> Rule | None:
    for rule in rules:
        if rule.group_id == group_id and rule.user_id == user_id:
            return rule
    return None
