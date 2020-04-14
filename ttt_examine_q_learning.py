# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:58:57 2019

@author: daugh
"""
from ttt_play import State
from ttt_policies import TabularPolicy
import os
import pickle

policy, i_epoch = pickle.load(open(os.path.dirname(
    os.getcwd()) + '/policy_evaluation.pkl', 'rb'))

print('This value function has been trained for %i epochs.' % i_epoch)
theta = 0.01
print('Accuracy %f' % theta)

opponent_policy = TabularPolicy(epsilon=1)
results = []
for i in range(1000):
    state = State()
    while True:
        state = State(from_base10 = policy.move_dict[state.get_num()])
        if state.is_terminal():
            break
        else:
            state = State(from_base10 = opponent_policy.move(state.get_num()))
            if state.is_terminal():
                break
    results.append(state.get_reward())
                
print("Average reward %f over 1000 games as player X against random policy." % (sum(results) / 1000.))

results = []
for i in range(1000):
    state = State()
    while True:
        state = State(from_base10 = opponent_policy.move(state.get_num()))
        if state.is_terminal():
            break
        else:
            state = State(from_base10 = policy.move_dict[state.get_num()])
            if state.is_terminal():
                break
    results.append(state.get_reward())
                
print("Average reward %f over 1000 games as player O against random policy." % (sum(results) / 1000.))