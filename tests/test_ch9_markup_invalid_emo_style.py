import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "chapter9" / "controllable-tts"))

from markup import parse


def test_markup_parse_normalizes_unknown_emo_and_style_tags():
    """Unrecognized EMO and STYLE tags must fall back to neutral/formal defaults."""
    segments = parse("[EMO: dramatic][STYLE: theatrical] Hello world")
    speech = [s for s in segments if s["type"] == "speech"]
    assert len(speech) == 1
    assert speech[0]["emotion"] == "neutral"
    assert speech[0]["style"] == "formal"
    assert speech[0]["text"] == "Hello world"
