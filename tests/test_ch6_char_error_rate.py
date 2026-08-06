import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TTS_DIR = HERE / "chapter6" / "tts-quality-eval"
if str(TTS_DIR) not in sys.path:
    sys.path.insert(0, str(TTS_DIR))

sys.modules.pop("config", None)

import pipeline


def test_char_error_rate_empty_reference_with_hypothesis():
    res = pipeline.char_error_rate("!!!", "hello")
    assert res.accuracy == 0.0
    assert res.edits == 5
    assert res.cer > 0.0


def test_char_error_rate_both_empty():
    res = pipeline.char_error_rate("!!!", "???")
    assert res.accuracy == 1.0
    assert res.edits == 0
    assert res.cer == 0.0
