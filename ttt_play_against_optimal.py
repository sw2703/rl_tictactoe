# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 06:57:48 2019

@author: josephwang
"""
from ttt_play import State
import os
import pickle

class EvaluateAgainstOptimal:
     def __init__(self, optimal_policy_path):
          """ Load an optimal policy
          """
          optimal_policy_path = os.path.dirname(os.getcwd()) + '/optimal_policy.pkl'
          self.optimal_policy, _ = pickle.load(open(optimal_policy_path, 'rb'))
          print("Optimal policy loaded.")

""" Load the policy to be evaluated 
"""
policy_path = os.path.dirname(os.getcwd()) + '/policy_evaluation.pkl'
policy, i_epoch = pickle.load(open(policy_path, 'rb'))
print("Policy loaded. This policy has been trained for %i epoches." % i_epoch)

""" Evaluate the performance of the policy as player X
"""
result_as_x = AutoPlay(policy, optimal_policy)

""" Evaluate the performance of the policy as player O
"""
result_as_o = AutoPlay(optimal_policy, policy)


def AutoPlay(policy_1, policy_2, n_games=100):
     """ Let policy_1 and policy_2 play against each other for n_games
     Input: self explanatory.
     Returns:
          A list of game results, i.e. reward for player 1.
     """
     game_results = []
     for i in range(n_games):
          state = get_initial_state()
          if state.turn == 2:
               state = State(from_base10 = policy_2.move_dict[state.get_num()])
          while not state.is_terminal():
               state = State(from_base10 = policy_1.move_dict[state.get_num()])
               if state.is_terminal():
                    break
               state = State(from_base10 = policy_2.move_dict[state.get_num()])
          game_results.append(state.get_reward())
     return game_results