"""Final Answer: a/b must evaluate the quotient for verify(), not the numerator."""

import sys
from types import ModuleType

try:
    import openai  # noqa: F401
except ImportError:
    _oai = ModuleType("openai")

    class _AsyncOpenAI:
        def __init__(self, *a, **k):
            pass

    _oai.AsyncOpenAI = _AsyncOpenAI
    sys.modules["openai"] = _oai

import generate_data as gd


def test_final_answer_slash_evaluates_to_quotient():
    assert gd.extract_predicted_number("Final Answer: 6/2") == 3.0
    assert gd.verify("Final Answer: 6/2", 3) is True
    assert gd.verify("Final Answer: 6/2", 6) is False


def test_plain_final_answer_unchanged():
    assert gd.extract_predicted_number("Final Answer: 42") == 42.0
    assert gd.verify("Final Answer: 42", 42) is True


def test_comma_thousands_still_works():
    assert gd.extract_predicted_number("Final Answer: 1,234") == 1234.0
