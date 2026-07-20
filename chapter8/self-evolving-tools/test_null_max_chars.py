"""Null optional max_chars must use default 6000."""
import base_tools


def test_null_max_chars_like_omit(monkeypatch):
    class Resp:
        text = "<html><title>T</title><body>" + ("word " * 2000) + "</body></html>"
        def raise_for_status(self):
            return None

    monkeypatch.setattr(base_tools.requests, "get", lambda *a, **k: Resp())
    out = base_tools.read_webpage("https://example.com", max_chars=None)
    assert out["success"] is True
    assert len(out["text"]) == 6000
    assert out["truncated"] is True
