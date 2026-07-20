"""Null optional num_results must use default 5."""
import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
import search_tools
from search_tools import search_web


def test_null_num_results_defaults_to_five():
    seen = {}

    class Resp:
        text = """
        <html><body>
          <div class="result">
            <a class="result__a" href="https://example.com">Example</a>
            <a class="result__snippet">snippet here</a>
          </div>
        </body></html>
        """
        def raise_for_status(self):
            return None

    real_min = min

    def tracking_min(a, b):
        seen["validated"] = real_min(a, b)
        return seen["validated"]

    with patch.object(search_tools.requests, "post", return_value=Resp()):
        with patch("builtins.min", side_effect=tracking_min):
            out = asyncio.run(search_web("q", num_results=None))
    payload = json.loads(out.text)
    assert payload["success"] is True
    assert seen.get("validated") == 5
