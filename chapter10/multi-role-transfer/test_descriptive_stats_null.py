"""JSON null elements in numbers must not crash descriptive_stats with float(None)."""
from tools import descriptive_stats


def test_null_element_skipped():
    out = descriptive_stats([1, None, 3])
    assert "样本量=2" in out
    assert "均值=2.0000" in out
    assert "最小=1.0" in out
    assert "最大=3.0" in out


def test_all_null_elements_empty_message():
    assert descriptive_stats([None, None]) == "输入为空，无法统计。"


def test_plain_numbers_unchanged():
    out = descriptive_stats([10, 20])
    assert "样本量=2" in out
    assert "均值=15.0000" in out
