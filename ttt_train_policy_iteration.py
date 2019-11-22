from ttt_play import State
from ttt_policies import TabularPolicy
import numpy as np
import os
import pickle
import time

class Train:
     def __init__(self, write_path, read_path = None):
          """
          Input:
               n_game: number of games to train for
               read_path, write_path: paths for reading or saving the model
          """
          self.read_path = read_path
          self.write_path = write_path
          if read_path:
               self.policy_1, self.i_epoch = pickle.load(open(self.read_path, 'rb'))
          else:
               self.policy_1 = TabularPolicy()
               self.i_epoch = 0
          self.policy_2 = TabularPolicy()  
          self.PolicyIteration()
          
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
                    s = State(from_base10 = num)  # here s is afterstate
                    
                    # terminal state, v function equals game result (no reward for transition)
                    if s.is_terminal():
                         self.policy_1.v_dict[num] = s.get_reward()
                    else:
                         # non-terminal afterstates
                         opponent_afterstate = State(from_base10 = self.policy_2.move_dict[num])
                         if opponent_afterstate.is_terminal():
                             self.policy_1.v_dict[num] = opponent_afterstate.get_reward()
                         else:
                             self.policy_1.v_dict[num] = self.policy_1.v_dict[opponent_afterstate.get_num()]

                    delta = max(delta, np.abs(v - self.policy_1.v_dict[num]))
               
               self.i_epoch += 1
               
               if delta < theta:
                    print('Value function has converged!')
                    print("Trained %i epochs so far." % self.i_epoch)
                    pickle.dump((self.policy_1, self.i_epoch), open(self.write_path, "wb" ) )
                    break
               
               if time.time() - t > 10:
                    t = time.time()
                    print("Trained %i epochs so far." % self.i_epoch)
                    pickle.dump((self.policy_1, self.i_epoch), open(self.write_path, "wb" ) )
     
     def PolicyImprovement(self):
          """ Policy Improvement following Sutton Barto 4.3
              Against rush opponent, with afterstates
          """
          self.policy_stable = True
          for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
               s = State(from_base10 = num)
               if not s.is_terminal():
                    old_action_num = self.policy_1.move_dict[num]
                    # get the best afterstates
                    afterstate_nums = s.legal_afterstates()
                    rewards = [State(from_base10 = x).get_reward() for x in afterstate_nums]
                    best = np.argmax(rewards)
                    self.policy_1.move_dict[num] = afterstate_nums[best]
                    if old_action_num != self.policy_1.move_dict[num]:
                        self.policy_stable = False
                    
     def PolicyIteration(self):
        """ Policy Iteration following Sutton Barto 4.3
              Against rush opponent, with afterstates
        """
        self.policy_stable = False
        while not self.policy_stable:
            self.PolicyEvaluation()
            self.PolicyImprovement()
        self.PolicyEvaluation()
        print('Policy iteration finished!')            
               
if __name__ == '__main__':
#     Train(read_path = r'C:\Users\daugh\Documents\GitHub\rl_tictactoe_data\policy_evaluation.pkl', write_path = r'C:\Users\daugh\Documents\GitHub\rl_tictactoe_data\policy_evaluation.pkl')               
     Train(write_path = os.path.dirname(os.getcwd()) + '/policy_evaluation.pkl')               