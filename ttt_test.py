# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 07:29:06 2019

@author: josephwang
"""

from ttt_play import State, Game
from ttt_policies import Policy, RushPolicy
import pytest


def test_initialize_state_from_base10():
    """ Legitimate number
    """
    num = int('1012012000', 3)
    state = State(from_base10 = num)
    assert state.board == [[0, 1, 2], [0, 1, 2], [0, 0, 0]]
    assert state.turn == 1
    
    """ Illegitimate number
    """
    num = int('120120120', 3)
    with pytest.raises(ValueError):
        state = State(from_base10 = num)  


def test_get_num_from_state():
    state = State(board = [[0, 1, 2], [0, 1, 2], [0, 0, 0]], turn = 2)
    num = state.get_num()
    assert num == int('2012012000', 3)
    state = State(board = [[1, 2, 1], [2, 1, 2], [1, 2, 2]])
    num = state.get_num()
    assert num == int('1121212122', 3)
    

def test_is_terminal():
  state = State(board = [[0, 2, 1], [0, 1, 2], [1, 2, 2]])
  assert not state.is_terminal()
  state = State(board = [[1, 2, 1], [2, 1, 2], [1, 2, 2]])
  assert state.is_terminal()


def test_random_policy():
    """
    Only one possible move.
    """
    state = State(board = [[1,2,1],[2,2,1],[0,1,2]], turn = 1)
    policy = Policy()
    state = policy.select_move(state).next_state()
    expected_state = State(board = [[1,2,1],[2,2,1],[1,1,2]], turn = 2)
    assert state.board == expected_state.board
    assert state.turn == expected_state.turn
    
    """
    Multiple possible moves.
    """
    state = State(board = [[1,0,0],[2,2,1],[0,1,2]], turn = 2)
    policy = Policy()
    state = policy.select_move(state).next_state()
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
    policy = Policy()
    with pytest.raises(RuntimeError):
        policy.select_move(state).next_state()
        
def test_rush_policy():
    """
    Only one possible move.
    """
    state = State(board = [[1,2,1],[2,2,1],[0,1,2]], turn = 1)
    policy = RushPolicy()
    state = policy.select_move(state).next_state()
    expected_state = State(board = [[1,2,1],[2,2,1],[1,1,2]], turn = 2)
    assert state.board == expected_state.board
    assert state.turn == expected_state.turn
    
    """
    Multiple possible moves.
    """
    state = State(board = [[1,0,0],[2,2,1],[0,1,2]], turn = 2)
    policy = RushPolicy()
    state = policy.select_move(state).next_state()
    expected_board = [[1,2,0],[2,2,1],[0,1,2]]
    assert state.board == expected_board
    assert state.turn == 1
    """
    Filled board
    """
    state = State(board = [[1,2,1],[2,2,1],[1,1,2]], turn = 2)
    policy = Policy()
    with pytest.raises(RuntimeError):
        policy.select_move(state).next_state()
        
def test_judge():
     # horizontal
     game = Game()
     game.state.board = [[0, 0, 0], [1, 1, 1], [0, 2, 2]]
     assert game.judge()== 1
     # vertical
     game = Game()
     game.state.board = [[0, 1, 2], [0, 1, 2], [1, 0, 2]]
     assert game.judge() == 2
     # diagonal 
     game = Game()
     game.state.board = [[1, 0, 2], [0, 1, 0], [0, 2, 1]]
     assert game.judge() == 1
     # unfinished game
     game = Game()
     game.state.board = [[1, 0, 0], [0, 0, 2], [0, 0, 0]]
     assert game.judge() == -1
     # tied game
     game = Game()
     game.state.board = [[1, 2, 2], [2, 1, 1], [2, 1, 2]]
     assert game.judge() == 0