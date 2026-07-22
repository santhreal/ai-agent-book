"""Regression: JSON null bullets must not crash narration/join paths.

Avoids importing demo.py (PIL) by extracting the helpers/functions under test.
"""
import ast
import json
import sys
from pathlib import Path


def _load_fns(*names):
    src = Path(__file__).with_name("demo.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    available = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    wanted = []
    for name in names:
        if name not in available:
            raise AssertionError(f"missing function {name} in demo.py")
        wanted.append(available[name])
    mod = ast.Module(body=wanted, type_ignores=[])
    ast.fix_missing_locations(mod)
    ns = {
        "json": json,
        "sys": sys,
        "Path": Path,
    }
    exec(compile(mod, "demo.py", "exec"), ns)
    return ns


def test_slide_bullets_null_like_empty():
    ns = _load_fns("slide_bullets")
    assert ns["slide_bullets"]({"bullets": None}) == []
    assert ns["slide_bullets"]({"bullets": ["a", "b"]}) == ["a", "b"]
    assert ns["slide_bullets"]({}) == []


def test_offline_narration_null_bullets():
    # Pristine demo joins slide['bullets'] directly (TypeError on null).
    # Fixed demo calls slide_bullets; load it when present.
    src = Path(__file__).with_name("demo.py").read_text(encoding="utf-8")
    names = ["offline_narration"]
    if "def slide_bullets" in src:
        names.append("slide_bullets")
    ns = _load_fns(*names)
    text = ns["offline_narration"](
        {"title": "T", "subtitle": "Intro", "bullets": None}
    )
    assert text == "Intro。。"


def test_load_slides_file_coerces_null_bullets(tmp_path: Path):
    ns = _load_fns("load_slides_file")
    path = tmp_path / "slides.json"
    path.write_text(
        json.dumps([{"title": "T", "subtitle": "S", "bullets": None}]),
        encoding="utf-8",
    )
    slides = ns["load_slides_file"](path)
    assert slides[0]["bullets"] == []
