"""Regression: non-dict parser returns must not TypeError crash parse_line."""
import pytest
from engine import LogParserEngine, ParseError, builtin_json_parser


def test_list_return_from_parser_skips_to_next():
    eng = LogParserEngine()
    eng.register("bad", lambda line: ["x"])
    eng.register("json", builtin_json_parser)
    out = eng.parse_line('{"timestamp":"t","level":"INFO","message":"m"}')
    assert out["_parser"] == "json"
    assert out["message"] == "m"


def test_only_bad_parser_raises_parse_error():
    eng = LogParserEngine()
    eng.register("bad", lambda line: ["x"])
    with pytest.raises(ParseError):
        eng.parse_line("not-json")
