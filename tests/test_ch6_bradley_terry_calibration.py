import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent.parent
ELO_DIR = HERE / "chapter6" / "elo-leaderboard"
if str(ELO_DIR) not in sys.path:
    sys.path.insert(0, str(ELO_DIR))

from bradley_terry import compute_mle_elo


def test_compute_mle_elo_calibration_model_default_none_rating():
    df = pd.DataFrame([
        {"model_a": "gpt-4", "model_b": "claude-3", "winner": "model_a"},
        {"model_a": "gpt-4", "model_b": "claude-3", "winner": "model_b"},
    ])
    res = compute_mle_elo(df, calibration_model="gpt-4")
    assert "gpt-4" in res.index
    assert res["gpt-4"] == 1000.0
