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
            self.policy_1, self.i_epoch = pickle.load(open(path, 'rb'))
            print('Policy read from file. Trained for %i epochs.' % self.i_epoch)
        else:
            self.policy_1 = TabularPolicy()
            self.i_epoch = 0
        self.policy_2 = TabularPolicy(
        )  # behavior policy, will be called to give epsilon-soft move with epsilon = 1, i.e. fullly random            
        self.path = path
        self.policy_stable = True

    def TrainContinuously(self):
        t = time.time()
        while True:
            while time.time() - t < 10:
                self.TrainOneRound()
                self.i_epoch += 1
            t = time.time()
            pickle.dump((self.policy_1, self.i_epoch),
                        open(self.path, "wb"))
            print("Trained %i epochs so far." % self.i_epoch)

    def TrainOneRound(self):
        """ Off-policy MC prediction following Sutton Barto 5.6
        """        
        c = {}
        trajectory = self.GetOneTrajectory()
        g = State(from_base10=trajectory[-1]).get_reward()  # g is a constant for our case
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

    def GetOneTrajectory(self):
        """ 
        Returns: list of state nums of a trajectory following the behavior policy, self.policy_2
        """
        num = State().get_num()
        trajectory = [num]
        while not State(from_base10=num).is_terminal():
            num = self.policy_2.epsilon_soft(num, epsilon=1)
            trajectory.append(num)
        return trajectory
    
if __name__ == '__main__':
    #        SelfPlayTrain(path=os.path.dirname(
    #            os.getcwd()) + '/policy_evaluation.pkl')
    Train(path=os.path.dirname(os.getcwd()) +
          '/policy_evaluation.pkl', read_first=False).OffPlicyMCPrediction()
