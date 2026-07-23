"""FINAL ANSWER / boxed a/b must evaluate to the integer quotient, not the numerator."""

import demo as cfm


def test_final_answer_slash_evaluates():
    assert cfm.extract_answer("FINAL ANSWER: 6/2") == 3
    assert cfm.extract_answer("FINAL ANSWER: 10/2") == 5


def test_boxed_slash_evaluates():
    assert cfm.extract_answer(r"\boxed{6/2}") == 3


def test_plain_integer_final_answer_unchanged():
    assert cfm.extract_answer("FINAL ANSWER: 42") == 42
    assert cfm.extract_answer(r"\boxed{7}") == 7


def test_non_divisible_slash_returns_none():
    assert cfm.extract_answer("FINAL ANSWER: 5/2") is None
