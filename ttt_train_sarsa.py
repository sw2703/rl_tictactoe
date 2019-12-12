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
            self.target_policy.epsilon = 0.3
            print('Policy read from file. Trained for %i epochs.' % self.i_epoch)
        else:
            self.target_policy = TabularPolicy(epsilon = 0.3)
            self.i_epoch = 0
        self.opponent_policy = TabularPolicy(epsilon=1)
        self.path = path
        # num for the state with an empty board and with player 1 to make a move.
        self.start_num = int('1' + '0' * 9, 3)
        self.counter = {}
        self.counter[24138] = 0

    def TrainContinuously(self, n_epoch=1e99):
        t = time.time()
        while self.i_epoch < n_epoch:
            while time.time() - t < 10 and self.i_epoch < n_epoch:
                # Target policy as player 1
                self.TrainOneRound(self.target_policy.move(self.start_num))
                self.i_epoch += 1
                # Target policy as player 2
                self.TrainOneRound(self.start_num)
            t = time.time()
            pickle.dump((self.target_policy, self.i_epoch),
                        open(self.path, "wb"))
            print("Trained %i epochs so far." % self.i_epoch)

    def TrainOneRound(self, afterstate_num, alpha=.1):
        """ Sarsa following Sutton and Barto 6.2
        Input:
            afterstate: the afterstate of target_policy to start trainng with
            Note that the opponent makes a move first, then the target policy.
        """
        afterstate = State(from_base10=afterstate_num)
        while not afterstate.is_terminal():
            beforestate_num = self.opponent_policy.move(afterstate.get_num())
            beforestate = State(from_base10=beforestate_num)
            if beforestate.is_terminal():
                r = beforestate.get_reward()
                self.target_policy.v_dict[afterstate.get_num(
                )] += alpha * (r - self.target_policy.v_dict[afterstate.get_num()])
                break
            else:
                self.target_policy.be_greedy([beforestate_num])
                s_prime_num = self.target_policy.move(beforestate_num)
                s_prime = State(from_base10=s_prime_num)
                r = s_prime.get_reward()
                self.target_policy.v_dict[afterstate.get_num(
                )] += alpha * (r + self.target_policy.v_dict[s_prime_num] - self.target_policy.v_dict[afterstate.get_num()])
                afterstate = s_prime
        self.target_policy.be_greedy([self.start_num])


if __name__ == '__main__':
    #        SelfPlayTrain(path=os.path.dirname(
    #            os.getcwd()) + '/policy_evaluation.pkl')
    Train(path=os.path.dirname(os.getcwd()) +
          '/policy_evaluation.pkl', read_first=True).TrainContinuously()
