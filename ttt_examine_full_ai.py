# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:58:57 2019

@author: daugh
"""
from ttt_play import State
import os
import pickle
import pytest

policy, i_epoch = pickle.load(open(os.path.dirname(
    os.getcwd()) + '/policy_evaluation.pkl', 'rb'))

print('This value function has been trained for %i epochs.' % i_epoch)
theta = 0.01
print('Accuracy %f' % theta)


state = State(board=[[1, 1, 1],
                     [2, 2, 1],
                     [2, 2, 1]], turn=2)
assert policy.v_dict[state.get_num()] == pytest.approx(
    1, abs=theta), 'Player 1 wins, expect value 1. Got %f' % policy.v_dict[state.get_num()]

state = State(board=[[1, 1, 2],
                     [2, 2, 1],
                     [1, 2, 1]], turn=2)
assert policy.v_dict[state.get_num()] == pytest.approx(
    0, abs=theta), 'Tied. Expect value 0. Got %f' % policy.v_dict[state.get_num()]

state = State(board=[[1, 1, 0],
                     [2, 2, 1],
                     [2, 1, 0]], turn=2)
assert policy.v_dict[state.get_num()] == pytest.approx(
    -1, abs=theta), 'One step before losing. Expect value -1. Got %f' % policy.v_dict[state.get_num()]

state = State(board=[[1, 1, 0],
                     [2, 2, 1],
                     [0, 2, 1]], turn=2)
assert policy.v_dict[state.get_num()] == pytest.approx(
    0, abs=theta), 'Two steps before a tie. Expect value 0. Got %f' % policy.v_dict[state.get_num()]

state = State(board=[[1, 1, 0],
                     [2, 1, 1],
                     [2, 2, 2]])
assert policy.v_dict[state.get_num()] == pytest.approx(
    -1, abs=theta), 'Player 2 wins, expect value -1. Got %f' % policy.v_dict[state.get_num()]

state = State(board=[[1, 1, 0],
                     [2, 2, 1],
                     [2, 2, 1]])
assert policy.v_dict[state.get_num()] == pytest.approx(
    1, abs=theta), 'Player 1 wins next step, expect value 1. Got %f' % policy.v_dict[state.get_num()]

state = State(board=[[1, 1, 2],
                     [2, 2, 1],
                     [0, 2, 1]])
assert policy.v_dict[state.get_num()] == pytest.approx(
    0, abs=theta), 'Will be tied next step, expect value 0. Got %f' % policy.v_dict[state.get_num()]

""" The following are specific for full AI
"""
state = State(board=[[0, 2, 0],
                     [0, 1, 0],
                     [0, 0, 0]])
afterstate_num = policy.move_dict[state.get_num()]
assert policy.v_dict[afterstate_num] == pytest.approx(
    1, abs=theta), 'Player 1 can win, expect value 1. Got %f' % policy.v_dict[state.get_num()]

state = State(board = [[2, 1, 0], [1, 1, 2], [0, 2, 0]], turn = 1)
afterstate_num = policy.move_dict[state.get_num()]
policy.print_progression(state)
assert policy.v_dict[afterstate_num] == pytest.approx(
    0, abs=theta), 'Will be a tie, expect value 0. Got %f' % policy.v_dict[state.get_num()]

assert policy.v_dict[afterstate_num] == pytest.approx(
    0, abs=theta), 'Will be tied, expect value 0. Got %f' % policy.v_dict[state.get_num()]

""" Keep this print statement at the end
"""
print('All assertions passed.')
