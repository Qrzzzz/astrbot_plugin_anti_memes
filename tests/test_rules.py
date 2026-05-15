from rules import find_rule, is_digits, migrate_targets_to_rules, normalize_targets


def test_is_digits():
    assert is_digits("123")
    assert not is_digits("1a")


def test_normalize_targets():
    assert normalize_targets({"1": ["2", "x", "2"]}) == {"1": ["2"]}


def test_migrate_targets_to_rules():
    rules = migrate_targets_to_rules({"targets": {"100": ["200"]}})
    assert len(rules) == 1 and rules[0].group_id == "100" and rules[0].user_id == "200"


def test_rule_match():
    rules = migrate_targets_to_rules({"targets": {"100": ["200"]}})
    assert find_rule(rules, "100", "200") is not None
    assert find_rule(rules, "100", "201") is None
