import sys
from pathlib import Path
import pandas as pd
import pytest

pytest.importorskip("pandas")

HERE = Path(__file__).resolve().parent.parent
ELO_DIR = HERE / "chapter6" / "elo-leaderboard"
if str(ELO_DIR) not in sys.path:
    sys.path.insert(0, str(ELO_DIR))

from elo_rating import EloRatingSystem  # noqa: E402
from leaderboard import compare_win_rates  # noqa: E402


def test_compare_win_rates_empty_df_columns():
    elo = EloRatingSystem()
    res = compare_win_rates(elo, pd.DataFrame())
    assert list(res.columns) == ["model_a", "model_b", "empirical", "predicted", "error"]
    assert len(res) == 0
    assert res["error"].empty
