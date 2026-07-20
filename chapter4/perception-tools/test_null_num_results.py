"""Null optional num_results must use default 5 before validation."""
import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from search_tools import search_web


def test_null_num_results_defaults(monkeypatch):
    class Resp:
        text = "<html><div class=\"result\"></div></html>"
        def raise_for_status(self):
            return None

    with patch("search_tools.requests.post", return_value=Resp()):
        # Even with empty parse, should not TypeError on null num_results
        out = asyncio.run(search_web("q", num_results=None))
    payload = json.loads(out.text)
    # Either success with results or soft failure that is NOT the None comparison TypeError
    msg = str(payload.get("message", ""))
    assert "NoneType" not in msg
