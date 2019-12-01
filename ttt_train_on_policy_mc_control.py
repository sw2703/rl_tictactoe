from ttt_play import State
from ttt_policies import TabularPolicy
import numpy as np
import os
import pickle
import time


class SelfPlayTrain:
    def __init__(self, path):
        self.path = path
        self.IterativeTrain()

    def IterativeTrain(self):
        trainer = TrainOneRound(path=self.path)
        trainer.OnPolicyMCControl()
        while not trainer.policy_stable:
            trainer = TrainOneRound(path=self.path, read_first=True)
            trainer.OnPolicyMCControl()
        print("Self play finished!")


class Train:
    def __init__(self, path, read_first=False, epsilon=0.1):
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
        self.epsilon = epsilon

    def OnPolicyMCControl(self):
        """ On-policy MC control following Sutton Barto 5.4
        """
        t = time.time()
        while True:
             while time.time() - t < 10:
                  returns = dict()
                  for s in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
                      returns[s] = []
                  num = State().get_num()
                  history = [num]
                  while not State(from_base10=num).is_terminal():
                      num = self.policy_1.epsilon_soft(num, self.epsilon)
                      history.append(num)
                  g = State(from_base10=num).get_reward()  # g is a constant for our case
                  for i, num in enumerate(history):
                      returns[num].append(g)
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
