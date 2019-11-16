# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:58:57 2019

@author: daugh
"""
from ttt_play import State
import pickle

policy, _ = pickle.load(open(r'C:\Users\daugh\Documents\GitHub\rl_tictactoe_data\policy_evaluation.pkl', 'rb'))

print('End state, expect value 0 even if a player wins.')
state = State(board = [[1, 1, 1], 
                       [2, 2, 1], 
                       [2, 2, 1]])
print('Value = %f' % policy.v_dict[state.get_num()])

