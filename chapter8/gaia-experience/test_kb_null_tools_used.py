"""Regression: JSON null tools_used must not crash keyword search join."""
import ast
from pathlib import Path
from typing import Any, Dict, List, Optional


def _load_keyword_search():
    src = Path(__file__).with_name("knowledge_base.py").read_text()
    tree = ast.parse(src)
    method = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "KnowledgeBase":
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "_keyword_search":
                    method = item
                    break
            break
    assert method is not None
    class_src = ast.Module(
        body=[
            ast.ClassDef(
                name="KnowledgeBase",
                bases=[],
                keywords=[],
                body=[method],
                decorator_list=[],
            )
        ],
        type_ignores=[],
    )
    ast.fix_missing_locations(class_src)
    ns = {"List": List, "Dict": Dict, "Any": Any, "Optional": Optional}
    exec(compile(class_src, "knowledge_base.py", "exec"), ns)

    class KB(ns["KnowledgeBase"]):
        def __init__(self, documents):
            self.documents = documents

    return KB


def test_keyword_search_null_tools_used():
    KB = _load_keyword_search()
    kb = KB([
        {
            "question": "How to search the web for GAIA answers?",
            "approach": "use web search",
            "tools_used": None,
        }
    ])
    results = kb._keyword_search("search web", top_k=3)
    assert len(results) == 1
    assert results[0]["question"].startswith("How to search")


def test_keyword_search_empty_tools_used():
    KB = _load_keyword_search()
    kb = KB([
        {
            "question": "How to search the web for GAIA answers?",
            "approach": "use web search",
            "tools_used": [],
        }
    ])
    results = kb._keyword_search("search web", top_k=3)
    assert len(results) == 1
