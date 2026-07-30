"""Tests for render_nl formatting in csp_solver."""
import pytest
from csp_solver import render_nl


def test_render_nl_unknown_node():
    node = ["unknown_tag", "A"]
    with pytest.raises(ValueError, match="未知的陈述节点"):
        render_nl(node)


def test_render_nl_and_compound_with_count_subclause():
    node = ["and", ["count", "knight", "==", 1], ["is", "A", "knight"]]
    result = render_nl(node)
    assert result == "我们当中恰好有 1 个骑士，并且 A 是骑士。"
