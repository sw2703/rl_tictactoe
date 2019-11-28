from ttt_play import State
from ttt_policies import TabularPolicy
import numpy as np
import os
import pickle
import time


class SelfPlayTrain():
    def __init__(self, path):
        self.path = path
        self.IterativeTrain()

    def IterativeTrain(self):
        trainer = TrainOneRound(write_path=self.path, self_play=True)
        while trainer.policy_ever_changed:
            trainer.ValueIteration()
        print("Self play finished!")


class TrainOneRound:
    def __init__(self, write_path, read_path=None, self_play=False):
        """
        Input:
             n_game: number of games to train for
             read_path, write_path: paths for reading or saving the model
        """
        self.read_path = read_path
        self.write_path = write_path
        if read_path:
            self.policy_1, self.i_epoch = pickle.load(
                open(self.read_path, 'rb'))
            print('Policy read from file. Trained for %i epochs.' % self.i_epoch)
        else:
            self.policy_1 = TabularPolicy()
            self.i_epoch = 0
            print('Training new policy.')
            self.read_path = self.write_path  # for later iterative training
        if self_play:
            self.policy_2 = self.policy_1
        else:
            self.policy_2 = TabularPolicy()
        self.policy_ever_changed = True  # Set to true to state iterative training

    def PolicyEvaluation(self):
        """Policy Evaluation following Sutton Barto 4.3
           Against rush opponent, with afterstates
        """
        theta = 0.01
        t = time.time()
        while True:
            delta = 0
            for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
                v = self.policy_1.v_dict[num]
                state = State(from_base10=num)  # here s is afterstate

                # terminal state, v function equals game result (no reward for transition)
                if state.is_terminal():
                    self.policy_1.v_dict[num] = state.get_reward()
                else:
                    # non-terminal afterstates
                    opponent_afterstate = State(
                        from_base10=self.policy_2.move_dict[num])
                    if opponent_afterstate.is_terminal():
                        self.policy_1.v_dict[num] = opponent_afterstate.get_reward(
                        )
                    else:
                        s_prime_num = self.policy_1.move_dict[opponent_afterstate.get_num(
                        )]
                        self.policy_1.v_dict[num] = self.policy_1.v_dict[s_prime_num]

                delta = max(delta, np.abs(v - self.policy_1.v_dict[num]))

            self.i_epoch += 1

            if delta < theta:
                print('Value function has converged!')
                print("Trained %i epochs so far." % self.i_epoch)
                pickle.dump((self.policy_1, self.i_epoch),
                            open(self.write_path, "wb"))
                break

            if time.time() - t > 10:
                t = time.time()
                print("Trained %i epochs so far." % self.i_epoch)
                pickle.dump((self.policy_1, self.i_epoch),
                            open(self.write_path, "wb"))

    def PolicyImprovement(self):
        """ Policy Improvement following Sutton Barto 4.3
            Against rush opponent, with afterstates
        """
        self.policy_stable = True
        for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
            state = State(from_base10=num)
            if not state.is_terminal():
                old_action_num = self.policy_1.move_dict[num]
                # get the best afterstates
                afterstate_nums = state.legal_afterstates()
                afterstate_values = [self.policy_1.v_dict[x]
                                     for x in afterstate_nums]
                best = np.argmax(afterstate_values) if state.turn == 1 else np.argmin(
                    afterstate_values)
                self.policy_1.move_dict[num] = afterstate_nums[best]
                if old_action_num != self.policy_1.move_dict[num]:
                    self.policy_stable = False
                    self.policy_ever_changed = True

    def PolicyIteration(self):
        """ Policy Iteration following Sutton Barto 4.3
              Against rush opponent, with afterstates
        """
        self.policy_stable = False
        self.policy_ever_changed = False
        while not self.policy_stable:
            self.PolicyEvaluation()
            self.PolicyImprovement()
        self.PolicyEvaluation()
        print('Policy iteration finished!')

    def ValueIteration(self, theta=0.01):
        t = time.time()
        while True:
            delta = 0
            for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
                v = self.policy_1.v_dict[num]
                state = State(from_base10=num)
                if state.is_terminal():
                    self.policy_1.v_dict[num] = state.get_reward()
                else:
                    opponent_afterstate = State(
                        from_base10=self.policy_2.move_dict[num])
                    if opponent_afterstate.is_terminal():
                        self.policy_1.v_dict[num] = opponent_afterstate.get_reward(
                        )
                    else:
                        s_prime_choices = opponent_afterstate.legal_afterstates()
                        vi_update = max([self.policy_1.v_dict[x]
                                         for x in s_prime_choices])
                        self.policy_1.v_dict[num] = vi_update
                delta = max(delta, np.abs(v - self.policy_1.v_dict[num]))

            self.i_epoch += 1

            if delta < theta:
                print('Value function has converged!')
                print("Trained %i epochs so far." % self.i_epoch)
                for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
                    s = State(from_base10=num)
                    if not s.is_terminal():
                        afterstates = s.legal_afterstates()
                        v_dict_slice = {
                            s: self.policy_1.v_dict[s] for s in afterstates}
                        old_move = self.policy_1.move_dict[num]
                        self.policy_1.move_dict[num] = max(
                            v_dict_slice, key=v_dict_slice.get)
                        if old_move != self.policy_1.move_dict[num]:
                            self.policy_ever_changed = True
                pickle.dump((self.policy_1, self.i_epoch),
                            open(self.write_path, "wb"))
                break

            if time.time() - t > 10:
                t = time.time()
                print("Trained %i epochs so far." % self.i_epoch)
                for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
                    s = State(from_base10=num)
                    if not s.is_terminal():
                        afterstates = s.legal_afterstates()
                        v_dict_slice = {
                            s: self.policy_1.v_dict[s] for s in afterstates}
                        old_move = self.policy_1.move_dict[num]
                        self.policy_1.move_dict[num] = max(
                            v_dict_slice, key=v_dict_slice.get)
                        if old_move != self.policy_1.move_dict[num]:
                            self.policy_ever_changed = True
                pickle.dump((self.policy_1, self.i_epoch),
                            open(self.write_path, "wb"))


if __name__ == '__main__':
    #     Train(read_path = r'C:\Users\daugh\Documents\GitHub\rl_tictactoe_data\policy_evaluation.pkl', write_path = r'C:\Users\daugh\Documents\GitHub\rl_tictactoe_data\policy_evaluation.pkl')
    SelfPlayTrain(path=os.path.dirname(os.getcwd()) + '/policy_evaluation.pkl')
