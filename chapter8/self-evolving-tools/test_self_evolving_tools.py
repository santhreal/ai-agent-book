import json
import tempfile
from pathlib import Path
from base_tools import web_search, read_webpage, code_interpreter
from tool_manager import ToolLibrary


def test_web_search_robustness():
    # Test query is None or not string
    res = web_search(None)
    assert not res["success"] or "query" in res

    res = web_search(123)
    assert "query" in res
    assert res["query"] == "123"

    # Test invalid num_results types
    res = web_search("NVDA", num_results=None)
    assert "query" in res

    res = web_search("NVDA", num_results="invalid")
    assert "query" in res


def test_read_webpage_robustness():
    # Test url is None or invalid type
    res = read_webpage(None)
    assert not res["success"]
    assert res["error"] == "invalid url"

    res = read_webpage(123)
    assert not res["success"]
    assert res["error"] == "invalid url"


def test_code_interpreter_robustness():
    # Test invalid code type
    res = code_interpreter(None)
    assert not res["success"]
    assert "code must be a string" in res["error"]

    # Test invalid pip_install type
    res = code_interpreter("print(1)", pip_install=123)
    assert not res["success"]
    assert "pip_install must be a list of strings" in res["error"]


def test_tool_library_robustness():
    with tempfile.TemporaryDirectory() as tmp_dir:
        library = ToolLibrary(library_dir=tmp_dir)

        # Test create_tool with invalid name type
        res = library.create_tool(None, "desc", {}, "def run(): pass")
        assert not res["success"]
        assert "tool name must be a string" in res["error"]

        # Create a malformed json file directly in the library
        p_malformed = Path(tmp_dir) / "malformed.json"
        p_malformed.write_text("invalid json")

        p_missing_fields = Path(tmp_dir) / "missing_fields.json"
        p_missing_fields.write_text(
            json.dumps({"name": "missing_fields"})
        )  # missing description

        p_valid = Path(tmp_dir) / "valid_tool.json"
        p_valid.write_text(
            json.dumps(
                {
                    "name": "valid_tool",
                    "description": "a valid tool",
                    "parameters": {"type": "object", "properties": {}},
                    "code": "def run(**kwargs):\n    return 'ok'",
                }
            )
        )

        # Test list_tools doesn't crash and filters out malformed JSON files
        tools = library.list_tools()
        assert len(tools) == 1
        assert tools[0]["name"] == "valid_tool"

        # Test get_tool doesn't crash on malformed JSON files
        assert library.get_tool("malformed") is None
        assert library.get_tool("missing_fields") is None
        assert library.get_tool("valid_tool") is not None
