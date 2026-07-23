"""Regression: negative top_k must return all hits, not drop the tail."""
import hashlib
import math

from discovery import ALL_TOOLS, ToolIndex


class _FakeEmbedder:
    name = "fake-test"

    def embed(self, texts):
        out = []
        for text in texts:
            digest = hashlib.md5(text.encode()).digest()
            vec = [(b / 255) - 0.5 for b in digest[:8]]
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            out.append([x / norm for x in vec])
        return out


def test_negative_top_k_returns_all():
    idx = ToolIndex(_FakeEmbedder(), tools=ALL_TOOLS[:8])
    all_hits = idx.search("stock price", top_k=8)
    assert len(idx.search("stock price", top_k=-1)) == len(all_hits)
    assert len(idx.search("stock price", top_k=-3)) == len(all_hits)


def test_positive_top_k_keeps_head():
    idx = ToolIndex(_FakeEmbedder(), tools=ALL_TOOLS[:8])
    assert len(idx.search("stock price", top_k=3)) == 3


def test_zero_top_k_empty():
    idx = ToolIndex(_FakeEmbedder(), tools=ALL_TOOLS[:8])
    assert idx.search("stock price", top_k=0) == []
