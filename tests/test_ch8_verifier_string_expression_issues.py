import os
import sys
from pathlib import Path

ch8_dir = Path(__file__).resolve().parent.parent / "chapter8" / "trajectory-verifier"
if str(ch8_dir) not in sys.path:
    sys.path.insert(0, str(ch8_dir))

from verifier import HeuristicQualityJudge, FAIL  # noqa: E402


def test_heuristic_quality_judge_string_expression_issues():
    judge = HeuristicQualityJudge()
    trajectory = {
        "quality_facts": {
            "expression_issues": [
                "raw string issue",
                {"turn": 2, "issue": "dict quality issue"},
            ]
        }
    }
    results = judge.evaluate(trajectory)
    expression_res = next(r for r in results if r.dimension == "expression_quality")
    assert expression_res.verdict == FAIL
    assert expression_res.evidence == [
        "issue: raw string issue",
        "turn 2: dict quality issue",
    ]
