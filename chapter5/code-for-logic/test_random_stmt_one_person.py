"""Regression: one-person puzzles must not IndexError in _random_stmt."""
import random
import sys
import types

sys.modules.setdefault("constraint", types.ModuleType("constraint"))
sys.modules["constraint"].Problem = object
import csp_solver as real_cs
cs = types.ModuleType("csp_solver")
cs.render_nl = real_cs.render_nl
cs.solve = real_cs.solve
cs.solve_labeled = real_cs.solve_labeled
sys.modules["csp_solver"] = cs

from build_puzzles import _random_stmt  # noqa: E402


def test_random_stmt_one_person_returns_count():
    rng = random.Random(0)
    for _ in range(20):
        stmt = _random_stmt("A", ["A"], rng)
        assert stmt[0] == "count"
        assert stmt[1] in ("knight", "knave")
