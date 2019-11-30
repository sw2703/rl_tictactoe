from ttt_play import State
from ttt_policies import TabularPolicy
import numpy as np
import os
import pickle
import time


class TrainOneRound:
    def __init__(self, read_path):
        """
        Input:
             read_path
        """
        self.read_path = read_path
        self.policy_1, self.i_epoch = pickle.load(open(self.read_path, 'rb'))
        print('Policy read from file. Trained for %i epochs.' % self.i_epoch)

    def MCPrediction(self, n_epoch):
        """ MC prediction following Sutton Barto 5.1
            Against rush opponent
        Input:
             n_epoch: the number of episodes to be trained
        """
        policy_1 = TabularPolicy()
        policy_2 = TabularPolicy()
        returns = dict()
        for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
             returns[num] = [0]
        for _ in range(n_epoch):
             # generate an episode following policy_1
             s = State().get_num()
             history = [s]
             while not State(from_base10 = s).is_terminal():
                  s = policy_1.move_dict[s]
                  history.append(s)
                  if State(from_base10 = s).is_terminal():
                       break
                  s = policy_2.move_dict[s]
                  history.append(s)
             # in our special case, g is a constant
             g = State(from_base10 = s).get_reward()
             for i, s in enumerate(history):
                  returns[s].append(g)
                  if i % 2 == 1:
                       policy_1.v_dict[s] = np.average(returns[s])
                  else:
                       policy_2.v_dict[s] = np.average(returns[s])
             
if __name__ == '__main__':
    #     Train(read_path = r'C:\Users\daugh\Documents\GitHub\rl_tictactoe_data\policy_evaluation.pkl', write_path = r'C:\Users\daugh\Documents\GitHub\rl_tictactoe_data\policy_evaluation.pkl')
    SelfPlayTrain(path=os.path.dirname(os.getcwd()) + '/policy_evaluation.pkl')
