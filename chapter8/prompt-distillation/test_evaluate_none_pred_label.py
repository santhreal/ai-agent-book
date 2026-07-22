"""Regression: unparseable model output (pred_label None) must not crash progress prints."""
import sys
import types

import pytest


def _stub_evaluate_deps() -> None:
    for name in [
        "torch",
        "numpy",
        "transformers",
        "peft",
        "tqdm",
    ]:
        sys.modules.setdefault(name, types.ModuleType(name))
    sys.modules["transformers"].AutoTokenizer = object
    sys.modules["transformers"].AutoModelForCausalLM = object
    sys.modules["peft"].PeftModel = object
    sys.modules["tqdm"].tqdm = lambda x, **k: x


_stub_evaluate_deps()

from evaluate import parse_language_label  # noqa: E402


def test_parse_language_label_returns_none_for_prose():
    assert parse_language_label("I believe this is English.") is None


def test_progress_format_tolerates_none_pred_label():
    from pathlib import Path

    src = Path(__file__).with_name("evaluate.py").read_text()
    assert "(pred_label or '??')" in src

    pred_label = parse_language_label("I believe this is English.")
    gt_label = "en"
    line = f"Pred: {(pred_label or '??'):>2s} | GT: {gt_label:>2s} |"
    assert "??" in line
    with pytest.raises(TypeError):
        f"{pred_label:>2s}"
