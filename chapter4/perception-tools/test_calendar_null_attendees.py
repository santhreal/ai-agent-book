"""Calendar events with attendees:null must format without TypeError."""

import asyncio
import json
import pickle
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock, mock_open, patch

SRC = Path(__file__).parent / "src"
sys.path.insert(0, str(SRC))

for name in (
    "dotenv",
    "mcp",
    "mcp.types",
    "requests",
    "pydantic",
    "googleapiclient",
    "googleapiclient.discovery",
    "google.oauth2",
    "google.oauth2.credentials",
    "google.auth",
    "google.auth.transport",
    "google.auth.transport.requests",
    "google_auth_oauthlib",
    "google_auth_oauthlib.flow",
):
    if name not in sys.modules:
        sys.modules[name] = ModuleType(name)

sys.modules["dotenv"].load_dotenv = lambda *a, **k: None
sys.modules["mcp.types"].TextContent = lambda **kw: SimpleNamespace(**kw)


class _BaseModel:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def model_dump(self):
        return dict(self.__dict__)


def _Field(default=None, default_factory=None, **kw):
    if default_factory is not None:
        return default_factory()
    return default


sys.modules["pydantic"].BaseModel = _BaseModel
sys.modules["pydantic"].Field = _Field
sys.modules["google.oauth2.credentials"].Credentials = object
sys.modules["google.auth.transport.requests"].Request = object

import private_data_tools as pdt  # noqa: E402


def _run(coro):
    return asyncio.run(coro)


def _call_with_events(events_result):
    service = MagicMock()
    service.events.return_value.list.return_value.execute.return_value = events_result
    sys.modules["googleapiclient.discovery"].build = MagicMock(return_value=service)
    creds = SimpleNamespace(expired=False, refresh_token=None)
    with patch.object(pdt.os.path, "exists", return_value=True), \
            patch("builtins.open", mock_open()), \
            patch.object(pickle, "load", return_value=creds):
        return _run(pdt.get_calendar_events())


def test_null_attendees_like_empty_list():
    out = _call_with_events({
        "items": [
            {
                "id": "evt1",
                "summary": "Sync",
                "start": {"dateTime": "2026-07-21T10:00:00Z"},
                "end": {"dateTime": "2026-07-21T11:00:00Z"},
                "attendees": None,
            }
        ]
    })
    payload = json.loads(out.text)
    assert payload["success"] is True
    assert payload["message"]["events"][0]["attendees"] == []


def test_attendees_list_still_extracted():
    out = _call_with_events({
        "items": [
            {
                "id": "evt2",
                "summary": "Meet",
                "start": {"dateTime": "2026-07-21T12:00:00Z"},
                "end": {"dateTime": "2026-07-21T13:00:00Z"},
                "attendees": [{"email": "a@example.com"}, {"email": "b@example.com"}],
            }
        ]
    })
    payload = json.loads(out.text)
    assert payload["message"]["events"][0]["attendees"] == [
        "a@example.com", "b@example.com"]
