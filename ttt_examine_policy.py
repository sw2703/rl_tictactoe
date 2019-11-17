# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:58:57 2019

@author: daugh
"""
from ttt_play import State
import pickle
import pytest

policy, i_epoch = pickle.load(open(r'C:\Users\daugh\Documents\GitHub\rl_tictactoe_data\policy_evaluation.pkl', 'rb'))

print('This value function has been trained for %i epochs.' % i_epoch)
theta = 0.01
print('Value iteration, rush policy against rush opponent. Accuracy %f' % theta)

state = State(board = [[1, 1, 1], 
                       [2, 2, 1], 
                       [2, 2, 1]])
assert policy.v_dict[state.get_num()] == pytest.approx(0, abs = theta), 'End state, expect value 0 even if a player wins. Got %f' % policy.v_dict[state.get_num()]

state = State(board = [[1, 1, 2], 
                       [2, 2, 1], 
                       [0, 2, 1]])
assert policy.v_dict[state.get_num()] == pytest.approx(0, abs = theta), 'One step before a draw. Expect value 0. Got %f' % policy.v_dict[state.get_num()]

state = State(board = [[1, 1, 0], 
                       [2, 2, 1], 
                       [2, 2, 1]])
assert policy.v_dict[state.get_num()] == pytest.approx(1, abs = theta), 'The only choice is a winning move. Expect value 1. Got %f' % policy.v_dict[state.get_num()]

state = State(board = [[1, 1, 0], 
                       [2, 2, 0], 
                       [0, 0, 0]])
assert policy.v_dict[state.get_num()] == pytest.approx(1, abs = theta), 'The first choice among many is a winning move. Expect value 1. Got %f' % policy.v_dict[state.get_num()]

state = State(board = [[1, 2, 0], 
                       [2, 2, 0], 
                       [1, 1, 0]])
assert policy.v_dict[state.get_num()] == pytest.approx(-1, abs = theta), 'The first choice among many is a losing move. Expect value -1. Got %f' % policy.v_dict[state.get_num()] 

state = State(board = [[2, 2, 0], 
                       [2, 2, 0], 
                       [0, 0, 0]])
assert policy.v_dict[state.get_num()] == pytest.approx(-1, abs = theta), 'About to lose no matter what move is taken. Expect value -1. Got %f' % policy.v_dict[state.get_num()] 

""" Keep this print statement at the end
"""
print('All assertions passed.')