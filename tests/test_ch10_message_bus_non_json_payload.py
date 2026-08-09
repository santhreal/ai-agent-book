import os
import sys
from datetime import datetime
from pathlib import Path

ch10_pwr = Path(__file__).resolve().parent.parent / "chapter10" / "parallel-web-research"
if str(ch10_pwr) not in sys.path:
    sys.path.insert(0, str(ch10_pwr))

from message_bus import Envelope  # noqa: E402


def test_envelope_short_non_json_payload():
    payload = {
        "created_at": datetime(2026, 1, 1, 12, 0, 0),
        "tags": {1, 2, 3},
    }
    env = Envelope(sender_id="agent1", target="agent2", type="update", payload=payload)
    short_str = env.short()
    assert isinstance(short_str, str)
    assert "agent1" in short_str
    assert "agent2" in short_str
    assert "update" in short_str
    assert "2026-01-01" in short_str
