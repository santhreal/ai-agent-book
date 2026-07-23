"""_frange must not hang when step is zero or negative."""

from pathlib import Path

import pytest

from agents import _frange


def test_zero_step_raises_instead_of_hanging():
    with pytest.raises(ValueError, match="step must be positive"):
        _frange(0, 10, 0)


def test_negative_step_raises_instead_of_hanging():
    with pytest.raises(ValueError, match="step must be positive"):
        _frange(0, 10, -1)


def test_positive_step_still_samples():
    assert _frange(0, 1, 0.5) == [0, 0.5]


def test_source_guards_nonpositive_step():
    text = Path(__file__).with_name("agents.py").read_text(encoding="utf-8")
    assert "if step <= 0:" in text
    assert "step must be positive" in text
