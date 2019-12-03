# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 07:29:06 2019

@author: josephwang
"""

from ttt_play import State
from ttt_policies import TabularPolicy
from ttt_train_off_policy_mc_prediction import Train
import pytest


def test_initialize_state_from_base10():
    """ Legitimate number
    """
    num = int('1012012000', 3)
    state = State(from_base10=num)
    assert state.board == [[0, 1, 2], [0, 1, 2], [0, 0, 0]]
    assert state.turn == 1

    """ Illegitimate number
    """
    num = int('120120120', 3)
    with pytest.raises(ValueError):
        state = State(from_base10=num)


def test_get_num_from_state():
    state = State(board=[[0, 1, 2], [0, 1, 2], [0, 0, 0]], turn=2)
    num = state.get_num()
    assert num == int('2012012000', 3)
    state = State(board=[[1, 2, 1], [2, 1, 2], [1, 2, 2]])
    num = state.get_num()
    assert num == int('1121212122', 3)


def test_is_terminal():
    """ Board not full, but player 1 has won
    """
    state = State(board=[[0, 2, 1], [0, 1, 2], [1, 2, 2]])
    assert state.is_terminal()
    """ Board full
  """
    state = State(board=[[1, 2, 1], [2, 1, 2], [1, 2, 2]])
    assert state.is_terminal()


def test_judge():
    # horizontal
    state = State(board=[[0, 0, 0], [1, 1, 1], [0, 2, 2]], turn=1)
    assert state.judge() == 1
    # vertical
    state = State(board=[[0, 1, 2], [0, 1, 2], [1, 0, 2]], turn=1)
    assert state.judge() == 2
    # diagonal
    state = State(board=[[1, 0, 2], [0, 1, 0], [0, 2, 1]], turn=1)
    assert state.judge() == 1
    # unfinished game
    state = State(board=[[1, 0, 0], [0, 0, 2], [0, 0, 0]], turn=1)
    assert state.judge() == -1
    # tied game
    state = State(board=[[1, 2, 2], [2, 1, 1], [2, 1, 2]], turn=1)
    assert state.judge() == 0


def test_legal_afterstates():
    # full board, no legal afterstate
    state = State(board=[[2, 2, 2], [1, 1, 1], [1, 2, 2]], turn=1)
    assert not state.legal_afterstates()
    # one legal afterstate
    state = State(board=[[2, 2, 2], [1, 1, 1], [1, 0, 2]], turn=1)
    assert state.legal_afterstates() == [State(
        [[2, 2, 2], [1, 1, 1], [1, 1, 2]], turn=2).get_num()]
    # 3 legal afterstates
    state = State(board=[[2, 2, 2], [1, 1, 1], [0, 0, 0]], turn=2)
    temp = state.legal_afterstates()
    assert len(temp) == 3
    num1 = State(board=[[2, 2, 2], [1, 1, 1], [2, 0, 0]]).get_num()
    num2 = State(board=[[2, 2, 2], [1, 1, 1], [0, 2, 0]]).get_num()
    num3 = State(board=[[2, 2, 2], [1, 1, 1], [0, 0, 2]]).get_num()
    assert set(temp) == set([num1, num2, num3])


def test_rush_policy():
    """
    Only one possible move.
    """
    state = State(board=[[1, 2, 1], [2, 2, 1], [0, 1, 2]], turn=1)
    policy = TabularPolicy()
    after_state = State(from_base10=policy.move_dict[state.get_num()])
    expected_after_state = State(
        board=[[1, 2, 1], [2, 2, 1], [1, 1, 2]], turn=2)
    assert after_state.board == expected_after_state.board
    assert after_state.turn == expected_after_state.turn

    """
    Multiple possible moves.
    """
    state = State(board=[[1, 0, 0], [2, 2, 1], [0, 1, 2]], turn=2)
    policy = TabularPolicy()
    after_state = State(from_base10=policy.move_dict[state.get_num()])
    expected_board = [[1, 2, 0], [2, 2, 1], [0, 1, 2]]
    assert after_state.board == expected_board
    assert after_state.turn == 1
    """
    Filled board
    """
    state = State(board=[[1, 2, 1], [2, 2, 1], [1, 1, 2]], turn=2)
    policy = TabularPolicy()
    with pytest.raises(KeyError):
        after_state = State(from_base10=policy.move_dict[state.get_num()])


def test_be_greedy():
    policy = TabularPolicy()
    best = State(board=[[0, 0, 0], [1, 0, 0], [0, 0, 0]], turn=2)
    policy.v_dict[best.get_num()] = 1
    assert policy.be_greedy()
    state = State()
    assert policy.move_dict[state.get_num()] == best.get_num()
    assert not policy.be_greedy()  # No more change when run the second time

def test_get_trajectory():
    trainer = Train(path = 'foo', read_first = False)
    trainer.epsilon  = 0
    trajectory = trainer.GetOneTrajectory()
    num1 = State(board=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]).get_num()
    num2 = State(board=[[1, 0, 0], [0, 0, 0], [0, 0, 0]], turn=2).get_num()
    num3 = State(board=[[1, 2, 0], [0, 0, 0], [0, 0, 0]]).get_num()
    num4 = State(board=[[1, 2, 1], [0, 0, 0], [0, 0, 0]], turn=2).get_num()
    num5 = State(board=[[1, 2, 1], [2, 0, 0], [0, 0, 0]]).get_num()
    num6 = State(board=[[1, 2, 1], [2, 1, 0], [0, 0, 0]], turn=2).get_num()
    num7 = State(board=[[1, 2, 1], [2, 1, 2], [0, 0, 0]]).get_num()
    num8 = State(board=[[1, 2, 1], [2, 1, 2], [1, 0, 0]], turn=2).get_num()
    assert trajectory == [num1, num2, num3, num4, num5, num6, num7, num8]