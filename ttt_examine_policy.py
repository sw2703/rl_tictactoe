# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:58:57 2019

@author: daugh
"""
from ttt_play import State
import pickle

policy, i_epoch = pickle.load(open(r'C:\Users\daugh\Documents\GitHub\rl_tictactoe_data\policy_evaluation.pkl', 'rb'))

print('This value function has been trained for %i epochs.' % i_epoch)

print('End state, expect value 0 even if a player wins.')
state = State(board = [[1, 1, 1], 
                       [2, 2, 1], 
                       [2, 2, 1]])
print('Value = %f' % policy.v_dict[state.get_num()])

print('One step before a draw. Expect value 0.')
state = State(board = [[1, 1, 2], 
                       [2, 2, 1], 
                       [0, 2, 1]])
print('Value = %f' % policy.v_dict[state.get_num()])

print('A state from which the only choice is a winning move. Expect value 1.')
state = State(board = [[1, 1, 0], 
                       [2, 2, 1], 
                       [2, 2, 1]])
print('Value = %f' % policy.v_dict[state.get_num()])

print('One choice among many is a winning move. Expect value 1.')
state = State(board = [[1, 1, 0], 
                       [2, 2, 0], 
                       [0, 0, 0]])
print('Value = %f' % policy.v_dict[state.get_num()])
