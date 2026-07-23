"""Only-seer-alive night must not IndexError on empty check candidates."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from werewolf.agent import PlayerAgent
from werewolf.game import Judge
from werewolf.roles import Role


def test_seer_act_alone_returns_without_crash():
    seer = PlayerAgent("P1", Role.SEER, offline=True)
    wolf = PlayerAgent("P2", Role.WEREWOLF, offline=True)
    wolf.alive = False
    judge = Judge([seer, wolf], seed=1)
    # No other living players to inspect — sibling _wolves_act already guards this.
    judge._seer_act()
    assert seer.alive is True


def test_seer_act_with_candidate_still_runs():
    seer = PlayerAgent("P1", Role.SEER, offline=True)
    villager = PlayerAgent("P2", Role.VILLAGER, offline=True)
    judge = Judge([seer, villager], seed=1)
    judge._seer_act()
    assert seer.alive is True
    assert villager.alive is True
