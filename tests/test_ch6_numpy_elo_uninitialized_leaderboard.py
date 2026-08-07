import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ELO_DIR = HERE / "chapter6" / "elo-leaderboard"
if str(ELO_DIR) not in sys.path:
    sys.path.insert(0, str(ELO_DIR))

from optimized_elo import NumpyEloRatingSystem  # noqa: E402


def test_numpy_elo_uninitialized_get_leaderboard():
    elo = NumpyEloRatingSystem()
    leaderboard = elo.get_leaderboard()
    assert leaderboard == []
