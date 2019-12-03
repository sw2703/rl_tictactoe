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
        self.opponent_policy = TabularPolicy(
        )  # will be called to give epsilon-soft move with epsilon = 1, i.e. fully random
        self.behavior_policy = TabularPolicy(
        )  # behavior policy, will be called to give epsilon-soft move with epsilon = 1, i.e. fully random
        self.path = path
        self.policy_stable = True
        self.epsilon = 0.1

    def TrainContinuously(self, n_epoch=1e24):
        t = time.time()
        while self.i_epoch < n_epoch:
            while time.time() - t < 10 and self.i_epoch < n_epoch:
                self.TrainOneRound()
                self.i_epoch += 1
            t = time.time()
            pickle.dump((self.policy_1, self.i_epoch),
                        open(self.path, "wb"))
            print("Trained %i epochs so far." % self.i_epoch)

    def TrainOneRound(self):
        """ Off-policy MC prediction following Sutton Barto 5.6
        """
        # behavior policy playing player 1
        trajectory = self.GetOneTrajectory(
            self.behavior_policy, self.opponent_policy)
        self.MCPredictIncremental(trajectory)
        # behavior policy playing player 2
        trajectory = self.GetOneTrajectory(
            self.opponent_policy, self.behavior_policy)
        self.MCPredictIncremental(trajectory)

    def GetOneTrajectory(self, policy_1, policy_2):
        """ 
        Returns: list of state nums of a trajectory
        """
        num = State().get_num()
        trajectory = [num]
        while not State(from_base10=num).is_terminal():
            num = policy_1.move(num)
            trajectory.append(num)
        return trajectory

    def MCPredictIncremental(self, trajectory):
        """ Incremental implementation of off-policy MC prediction
        """
        c = {}
        # g is a constant for our case
        g = State(from_base10=trajectory[-1]).get_reward()
        w = 1.
        for i, state in reversed(list(enumerate(trajectory))):
            if w == 0:
                break
            if state in c:
                c[state] += w
            else:
                c[state] = w
            self.policy_1.v_dict[state] += w / \
                c[state] * (g - self.policy_1.v_dict[state])
            if i != 0 and self.policy_1.move_dict[trajectory[i-1]] != trajectory[i]:
                w = 0
            else:
                w = w / \
                    len(State(from_base10=trajectory[i-1]).legal_afterstates())


if __name__ == '__main__':
    #        SelfPlayTrain(path=os.path.dirname(
    #            os.getcwd()) + '/policy_evaluation.pkl')
    Train(path=os.path.dirname(os.getcwd()) +
          '/policy_evaluation.pkl', read_first=False).TrainContinuously(n_epoch=2)
