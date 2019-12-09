from ttt_play import State
from ttt_policies import TabularPolicy
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
            self.target_policy, self.i_epoch = pickle.load(open(path, 'rb'))
            print('Policy read from file. Trained for %i epochs.' % self.i_epoch)
        else:
            self.target_policy = TabularPolicy()
            self.i_epoch = 0
        self.opponent_policy = TabularPolicy(epsilon=1)
        self.path = path

    def TrainContinuously(self, n_epoch=1e99):
        t = time.time()
        while self.i_epoch < n_epoch:
            while time.time() - t < 10 and self.i_epoch < n_epoch:
                self.TrainOneRound()
                self.i_epoch += 1
            t = time.time()
            pickle.dump((self.target_policy, self.i_epoch),
                        open(self.path, "wb"))
            print("Trained %i epochs so far." % self.i_epoch)

    def TrainOneRound(self, alpha=0.1):
        """ TD(0) following Sutton and Barto 6.1
        """
        # Target policy as player 1
        state = State()
        while not state.is_terminal():
            if state.turn == 1:
                s_prime_num = self.target_policy.move(state.get_num())
            else:
                s_prime_num = self.opponent_policy.move(state.get_num())
            r = State(from_base10=s_prime_num).get_reward()
            self.target_policy.v_dict[state.get_num()] += alpha * (
                r + self.target_policy.v_dict[s_prime_num] - self.target_policy.v_dict[state.get_num()])
            state = State(from_base10=s_prime_num)
        self.target_policy.v_dict[state.get_num()] = state.get_reward()


if __name__ == '__main__':
    #        SelfPlayTrain(path=os.path.dirname(
    #            os.getcwd()) + '/policy_evaluation.pkl')
    Train(path=os.path.dirname(os.getcwd()) +
          '/policy_evaluation.pkl', read_first=True).TrainContinuously()
