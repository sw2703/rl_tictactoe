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

state = State()
afterstate_num=policy.move_dict[state.get_num()]
expected_afterstate = State(board=[[0, 0, 0], 
                                   [0, 1, 0], 
                                   [0, 0, 0]], turn=2)
State(from_base10=afterstate_num).print_board()
expected_afterstate.print_board()
assert afterstate_num == expected_afterstate.get_num()

state = State(board=[[0, 2, 0], 
                     [0, 1, 0], 
                     [0, 0, 0]])
state.print_board()
afterstate_num=policy.move_dict[state.get_num()]
assert policy.v_dict[afterstate_num] == pytest.approx(
    1, abs=theta), 'Player 1 can win, expect value 1. Got %f' % policy.v_dict[state.get_num()]

""" Keep this print statement at the end
"""
print('All assertions passed.')
