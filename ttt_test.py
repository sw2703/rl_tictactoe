# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 07:29:06 2019

@author: josephwang
"""

from ttt_play import State
from ttt_policies import TabularPolicy
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
  """ Board not full, but player 1 has won
  """   
  state = State(board = [[0, 2, 1], [0, 1, 2], [1, 2, 2]])
  assert state.is_terminal()
  """ Board full
  """
  state = State(board = [[1, 2, 1], [2, 1, 2], [1, 2, 2]])
  assert state.is_terminal()
  
        
def test_rush_policy():
    """
    Only one possible move.
    """
    state = State(board = [[1,2,1],[2,2,1],[0,1,2]], turn = 1)
    policy = TabularPolicy()
    after_state = State(from_base10 = policy.move_dict[state.get_num()])
    expected_after_state = State(board = [[1,2,1],[2,2,1],[1,1,2]], turn = 2)
    assert after_state.board == expected_after_state.board
    assert after_state.turn == expected_after_state.turn
    
    """
    Multiple possible moves.
    """
    state = State(board = [[1,0,0],[2,2,1],[0,1,2]], turn = 2)
    policy = TabularPolicy()
    after_state = State(from_base10 = policy.move_dict[state.get_num()])
    expected_board = [[1,2,0],[2,2,1],[0,1,2]]
    assert after_state.board == expected_board
    assert after_state.turn == 1
    """
    Filled board
    """
    state = State(board = [[1,2,1],[2,2,1],[1,1,2]], turn = 2)
    policy = TabularPolicy()
    with pytest.raises(KeyError):
         after_state = State(from_base10 = policy.move_dict[state.get_num()])
        
        
def test_judge():
     # horizontal
     state = State(board = [[0, 0, 0], [1, 1, 1], [0, 2, 2]], turn = 1)
     assert state.judge()== 1
     # vertical
     state = State(board = [[0, 1, 2], [0, 1, 2], [1, 0, 2]], turn = 1)
     assert state.judge() == 2
     # diagonal 
     state = State(board = [[1, 0, 2], [0, 1, 0], [0, 2, 1]], turn = 1)
     assert state.judge() == 1
     # unfinished game
     state = State(board = [[1, 0, 0], [0, 0, 2], [0, 0, 0]], turn = 1)
     assert state.judge() == -1     
     # tied game
     state = State(board = [[1, 2, 2], [2, 1, 1], [2, 1, 2]], turn = 1)
     assert state.judge() == 0      