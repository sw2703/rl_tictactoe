from ttt_play import State
from ttt_policies import TabularPolicy
import os
import pickle
import time


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
          
    def MCES(self):
        """ MC exploring start following Sutton Barto 5.3
            Against rush opponent
        """
        t = time.time()
        self.policy_1 = TabularPolicy()
        # No need to use a list of returns, since the game is deterministic
        for s in range(int('2' + '0' * 9, 3), int('2' * 10, 3) + 1):
             history = [s]
             while not State(from_base10 = s).is_terminal():
                  s = self.policy_1.move_dict[s]
                  history.append(s)
                  if State(from_base10 = s).is_terminal():
                       break
                  s = self.policy_1.move_dict[s]
                  history.append(s)
             # in our special case, g is a constant
             g = State(from_base10 = s).get_reward()
             for i, s in enumerate(history):
                  self.policy_1.v_dict[s] = g
             self.policy_1.be_greedy(history)
             self.i_epoch += 1
             if time.time() - t > 10:
                  t = time.time()
                  pickle.dump((self.policy_1, self.i_epoch),
                            open(self.path, "wb"))
                  print("Trained %i epochs so far." % self.i_epoch)
             
        pickle.dump((self.policy_1, self.i_epoch),
                            open(self.path, "wb"))
        print('MC prediction finished.')
             
if __name__ == '__main__':
    trainer = TrainOneRound(path=os.path.dirname(os.getcwd()) + '/policy_evaluation.pkl')
    trainer.MCES()
