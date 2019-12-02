from ttt_play import State
from ttt_policies import TabularPolicy
import numpy as np
import os
import pickle
import time

class Train:
    def __init__(self, path, read_first=False):
        """
        Input:
             path: the path to save the policy
             read_first: if true, read from the path first
        """
        if read_first:
            self.policy_1, self.i_epoch = pickle.load(open(path, 'rb'))
            print('Policy read from file. Trained for %i epochs.' % self.i_epoch)
        else:
            self.policy_1 = TabularPolicy()
            self.i_epoch = 0
        self.path = path
        self.policy_stable = True

    def OffPlicyMCPrediction(self):
        """ Off-policy MC prediction following Sutton Barto 5.6
        """
        policy_2 = TabularPolicy()  # behavior policy, will be called to give 
                                    # epsilon-soft move with epsilon = 1
                                    # i.e. fullly random
        t = time.time()
        while True:
             while time.time() - t < 10:
                  returns = {}
                  c = {}
                  num = State().get_num()
                  history = [num]
                  while not State(from_base10=num).is_terminal():
                      num = self.policy_2.epsilon_soft(num, epsilon = 1)
                      history.append(num)
                  g = State(from_base10=num).get_reward()  # g is a constant for our case
                  
                  
                  
                  
                  
                  
                  for i, num in enumerate(history):
                      if num in returns:
                           returns[num].append(g)
                      else:
                           returns[num] = [g]
                      self.policy_1.v_dict[num] = np.average(returns[num])
                  if self.policy_1.be_greedy(history):
                      self.policy_stable = False
                  self.i_epoch += 1
     
             t = time.time()
             pickle.dump((self.policy_1, self.i_epoch),
                        open(self.path, "wb"))
             print("Trained %i epochs so far." % self.i_epoch)


if __name__ == '__main__':
#        SelfPlayTrain(path=os.path.dirname(
#            os.getcwd()) + '/policy_evaluation.pkl')
    Train(path=os.path.dirname(os.getcwd()) +
                  '/policy_evaluation.pkl', read_first=True).OnPolicyMCControl()
