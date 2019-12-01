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
print('Policy iteration against rush opponent. Accuracy %f' % theta)


state = State()
assert policy.v_dict[state.get_num()] == pytest.approx(
    1, abs=theta), 'Player 1 wins, expect value 1. Got %f' % policy.v_dict[state.get_num()]

state = State(board=[[1, 0, 0], [0, 0, 0], [0, 0, 0]], turn=2)
assert policy.v_dict[state.get_num()] == pytest.approx(
    1, abs=theta), 'Player 1 wins, expect value 1. Got %f' % policy.v_dict[state.get_num()]

state = State(board=[[1, 2, 0], [0, 0, 0], [0, 0, 0]])
assert policy.v_dict[state.get_num()] == pytest.approx(
    1, abs=theta), 'Player 1 wins, expect value 1. Got %f' % policy.v_dict[state.get_num()]

""" Keep this print statement at the end
"""
print('All assertions passed.')
