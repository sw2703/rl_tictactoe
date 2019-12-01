# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 06:57:48 2019

@author: josephwang
"""
from ttt_play import State
import numpy as np
import os
import pickle
import random

class EvaluateAgainstOptimal:
     def __init__(self):
          """ Load an optimal policy
          """
          optimal_policy_path = os.path.dirname(os.getcwd()) + '/optimal_policy.pkl'
          self.optimal_policy, _ = pickle.load(open(optimal_policy_path, 'rb'))
          print("Optimal policy loaded.")

          """ Load the policy to be evaluated 
          """
          policy_path = os.path.dirname(os.getcwd()) + '/policy_evaluation.pkl'
          self.policy, i_epoch = pickle.load(open(policy_path, 'rb'))
          print("Policy loaded. This policy has been trained for %i epoches." % i_epoch)

     def Run(self):
          """ Evaluate the performance of the policy as player X
          """
          result_as_x = self.AutoPlay(self.policy, self.optimal_policy)
          assert 1 not in result_as_x  # Cannot defeat optimal policy
          print("%i ties and %i losses against optimal policy, playing X." % (result_as_x.count(0), result_as_x.count(-1)))
          
          """ Evaluate the performance of the policy as player O
          """
          result_as_o = self.AutoPlay(self.optimal_policy, self.policy)
          assert -1 not in result_as_o  # Cannot defeat optimal policy
          print("%i ties and %i losses against optimal policy, playing O." % (result_as_o.count(0), result_as_o.count(1)))

     def AutoPlay(self, policy_1, policy_2, n_games=100):
          """ Let policy_1 and policy_2 play against each other for n_games
          Input: self explanatory.
          Returns:
               A list of game results, i.e. reward for player 1.
          """
          game_results = []
          for i in range(n_games):
               state = self.GetInitialState()
               if state.turn == 2:
                    state = State(from_base10 = policy_2.move_dict[state.get_num()])
               while not state.is_terminal():
                    state = State(from_base10 = policy_1.move_dict[state.get_num()])
                    if state.is_terminal():
                         break
                    state = State(from_base10 = policy_2.move_dict[state.get_num()])
               game_results.append(state.get_reward())
          return game_results
     
     def GetInitialState(self):
          """ Return an initial state. 50% chance an empty board (turn = 1), 50% chance a board with a randomly placed X (turn = 2).
          """
          if np.random.rand() < 0.5:
               return State()
          else:
               choices = State().legal_afterstates()
               num = random.choice(choices)
               return State(from_base10 = num)
          
if __name__ == '__main__':
      EvaluateAgainstOptimal().Run()