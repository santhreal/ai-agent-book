"""Regression test for chess get_game_status when game is over by rule-based draw."""
import asyncio
import sys
from pathlib import Path
import chess

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "chapter4" / "collaboration-tools" / "src"))

import chess_tools


def test_chess_game_over_rule_based_draw_status():
    # Board with 75-move rule / 150 halfmoves draw condition
    board = chess.Board("8/8/8/8/8/8/R7/r6k w - - 150 1")
    assert board.is_game_over() is True
    assert board.is_checkmate() is False
    assert board.is_stalemate() is False
    
    chess_tools._game_board = board
    res = asyncio.run(chess_tools.get_game_status())
    assert res["success"] is True
    
    status = res["game_status"]
    assert status["is_game_over"] is True
    assert status["is_draw"] is True
    assert status["status_message"] != "Game in progress"
