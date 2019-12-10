from ttt_play import State
from ttt_policies import TabularPolicy
import numpy as np
import os
import pickle
import time


class Train:
    def __init__(self, path, read_first=False, epsilon=0.3):
        """
        Input:
             path: the path to save the policy
             read_first: if true, read from the path first
        """
        if read_first:
            self.policy_1, self.i_epoch = pickle.load(open(path, 'rb'))
            print('Policy read from file. Trained for %i epochs.' % self.i_epoch)
        else:
            self.policy_1 = TabularPolicy(epsilon = .1)
            self.i_epoch = 0
        self.path = path
        self.policy_stable = True
        self.epsilon = epsilon

    def OnPolicyMCControl(self):
        """ On-policy MC control following Sutton Barto 5.4
        """
        t = time.time()
        returns = dict()
        while True:
            while time.time() - t < 10:
                num = State().get_num()
                history = [num]
                while not State(from_base10=num).is_terminal():
                    num = self.policy_1.move(num)
                    history.append(num)
                # g is a constant for our case
                g = State(from_base10=num).get_reward()
                for i, num in enumerate(history):
                    if num in returns:
                        returns[num].append(g)
                    else:
                        returns[num] = [g]
                    self.policy_1.v_dict[num] = np.average(returns[num])
                    if num == 36531:
                        print(self.policy_1.v_dict[num])
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
          '/policy_evaluation.pkl', read_first=False).OnPolicyMCControl()
