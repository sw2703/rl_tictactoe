# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 07:29:06 2019

@author: daugh
"""

from ttt_generic import State, Engine
import pytest

def test_move():
    """
    Only one possible move.
    """
    state = State(board = [[1,2,1],[2,2,1],[0,1,2]], turn = 1)
    engine = Engine()
    state = engine.move(state)
    expected_state = State(board = [[1,2,1],[2,2,1],[1,1,2]], turn = 2)
    assert state.board == expected_state.board
    assert state.turn == expected_state.turn
    
    """
    Multiple possible moves.
    """
    state = State(board = [[1,0,0],[2,2,1],[0,1,2]], turn = 2)
    engine = Engine()
    state = engine.move(state)
    expected_boards = [
                [[1,2,0],[2,2,1],[0,1,2]],
                [[1,0,2],[2,2,1],[0,1,2]],
                [[1,0,0],[2,2,1],[2,1,2]]
            ]
    assert state.board in expected_boards
    assert state.turn == 1
    """
    Filled board
    """
    state = State(board = [[1,2,1],[2,2,1],[1,1,2]], turn = 2)
    engine = Engine()
    with pytest.raises(RuntimeError):
        engine.move(state)