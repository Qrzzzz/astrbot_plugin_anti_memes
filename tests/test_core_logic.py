from collections import OrderedDict

from core import mark_processed, normalize_targets, raw_message_has_image


def test_normalize_targets() -> None:
    data = {123: [456, "456", "789", "abc"], "x": ["1"], "100": "bad"}
    out = normalize_targets(data)
    assert out == {"123": ["456", "789"]}


def test_ordered_cache_lru() -> None:
    cache: OrderedDict[str, None] = OrderedDict()
    for i in range(1, 106):
        mark_processed(cache, str(i), 100)
    assert list(cache.keys())[0] == "6"
    assert list(cache.keys())[-1] == "105"
    assert len(cache) == 100


def test_raw_message_has_image() -> None:
    assert raw_message_has_image("[CQ:image,file=1.jpg]") is True
    assert raw_message_has_image([{"type": "image"}]) is True
    assert raw_message_has_image("hello") is False
