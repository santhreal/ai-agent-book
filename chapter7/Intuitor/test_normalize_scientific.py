"""Scientific notation in boxed answers must normalize to the full value."""

from evaluate_from_cache import extract_and_normalize_answer, normalize_number


def test_boxed_scientific_integer_power():
    assert extract_and_normalize_answer(r"\boxed{1e3}") == "1000"
    assert normalize_number("1e3") == "1000"


def test_boxed_scientific_with_decimal_mantissa():
    assert extract_and_normalize_answer(r"\boxed{1.5e2}") == "150"


def test_plain_integer_unchanged():
    assert extract_and_normalize_answer(r"\boxed{42}") == "42"
    assert extract_and_normalize_answer(r"\boxed{3.5}") == "3.5"
