import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "chapter1" / "search-codegen"))
from agent import GPT5NativeAgent


def test_gpt5_native_agent_null_response_citations():
    assert GPT5NativeAgent._citations(None) == []
    assert GPT5NativeAgent._citations("not a dict") == []
    assert GPT5NativeAgent._citations(123) == []
    assert GPT5NativeAgent._citations([]) == []


def test_gpt5_native_agent_null_response_output_text():
    assert GPT5NativeAgent._output_text(None) == ""
    assert GPT5NativeAgent._output_text("not a dict") == ""
    assert GPT5NativeAgent._output_text(123) == ""
    assert GPT5NativeAgent._output_text([]) == ""


def test_gpt5_native_agent_null_response_tool_items():
    assert GPT5NativeAgent._tool_items(None) == []
    assert GPT5NativeAgent._tool_items("not a dict") == []
    assert GPT5NativeAgent._tool_items(123) == []
    assert GPT5NativeAgent._tool_items([]) == []
