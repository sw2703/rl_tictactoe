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
        self.behavior_policy = TabularPolicy(epsilon=1)
        self.path = path
        self.policy_stable = True
        self.epsilon = 0.1

    def TrainContinuously(self, n_epoch=1e99):
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
        self.MCPredictIncremental(trajectory, 1)
        # behavior policy playing player 2
        trajectory = self.GetOneTrajectory(
            self.opponent_policy, self.behavior_policy)
        self.MCPredictIncremental(trajectory, 2)

    def GetOneTrajectory(self, policy_1, policy_2):
        """ 
        Returns: list of state nums of a trajectory
        """
        num = State().get_num()
        trajectory = [num]
        while not State(from_base10=num).is_terminal():
            num = policy_1.move(num)
            trajectory.append(num)
            if not State(from_base10=num).is_terminal():
                num = policy_2.move(num)
                trajectory.append(num)
            else:
                break
        return trajectory

    def MCPredictIncremental(self, trajectory, role_behavior_policy):
        """ Incremental implementation of off-policy MC prediction
        Input:
            trajectory
            role_behavior_policy: 1 or 2, denoting which player the behavior policy acted as in this trajectory
        """
        c = {}
        # g is a constant for our case
        g = State(from_base10=trajectory[-1]).get_reward()
        w = 1.
        i = len(trajectory) - 1
        while i >= 0:
            if (i % 2 + 1) == role_behavior_policy:
                if w == 0:
                    break
                state = trajectory[i]
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
