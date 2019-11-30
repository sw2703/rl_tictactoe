from ttt_play import State
from ttt_policies import TabularPolicy
import numpy as np
import os
import pickle


class TrainOneRound:
    def __init__(self, path, read_first = False):
        """
        Input:
             path: the path to save the policy
             read_first: if true, read from the path first
        """
        if read_first:
             self.policy_1, self.i_epoch = pickle.load(open(path, 'rb'))
             print('Policy read from file. Trained for %i epochs.' % self.i_epoch)
        self.path = path
        self.i_epoch = 0
          
    def MCPrediction(self, n_epoch):
        """ MC prediction following Sutton Barto 5.1
            Against rush opponent
        Input:
             n_epoch: the number of episodes to be trained
        """
        self.policy_1 = TabularPolicy()
        self.policy_2 = TabularPolicy()
        returns = dict()
        for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
             returns[num] = [0]
        for _ in range(n_epoch):
             # generate an episode following policy_1
             s = State().get_num()
             history = [s]
             while not State(from_base10 = s).is_terminal():
                  s = self.policy_1.move_dict[s]
                  history.append(s)
                  if State(from_base10 = s).is_terminal():
                       break
                  s = self.policy_2.move_dict[s]
                  history.append(s)
             # in our special case, g is a constant
             g = State(from_base10 = s).get_reward()
             for i, s in enumerate(history):
                  returns[s].append(g)
                  if i % 2 == 1:
                       self.policy_1.v_dict[s] = np.average(returns[s])
                  else:
                       self.policy_2.v_dict[s] = np.average(returns[s])
        self.i_epoch += 1
        pickle.dump((self.policy_1, self.i_epoch),
                            open(self.path, "wb"))
        print('MC prediction finished.')
             
if __name__ == '__main__':
    trainer = TrainOneRound(path=os.path.dirname(os.getcwd()) + '/policy_evaluation.pkl')
    trainer.MCPrediction(1)
