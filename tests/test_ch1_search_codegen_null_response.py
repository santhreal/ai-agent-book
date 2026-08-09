import sys
import importlib.util
from pathlib import Path

_module_path = Path(__file__).parent.parent / "chapter1" / "search-codegen" / "agent.py"
_spec = importlib.util.spec_from_file_location("ch1_search_codegen_agent", _module_path)
_sc_agent = importlib.util.module_from_spec(_spec)
sys.modules["ch1_search_codegen_agent"] = _sc_agent
_spec.loader.exec_module(_sc_agent)
GPT5NativeAgent = _sc_agent.GPT5NativeAgent


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
