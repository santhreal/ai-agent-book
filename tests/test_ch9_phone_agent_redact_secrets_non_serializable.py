import importlib.util
import sys
from pathlib import Path
from datetime import datetime

_module_path = Path(__file__).resolve().parent.parent / "chapter9" / "phone-agent" / "agent.py"
_spec = importlib.util.spec_from_file_location("ch9_phone_agent", _module_path)
_pa_agent = importlib.util.module_from_spec(_spec)
sys.modules["ch9_phone_agent"] = _pa_agent
_spec.loader.exec_module(_pa_agent)
_redact_secrets = _pa_agent._redact_secrets


class CustomObject:
    def __str__(self):
        return "<CustomObject representation>"


def test_redact_secrets_non_serializable_objects():
    payload = {
        "timestamp": datetime(2026, 8, 8, 12, 0, 0),
        "custom": CustomObject(),
        "api_key": "sk-12345678901234567890",
    }

    redacted = _redact_secrets(payload)

    assert redacted["api_key"] == "[REDACTED]"
    assert redacted["custom"] == "<CustomObject representation>"
    assert "2026-08-08" in redacted["timestamp"]
