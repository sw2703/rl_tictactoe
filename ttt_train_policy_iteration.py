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
          self.SelfPlay()
               
     def PolicyEvaluation(self):
          """Policy Evaluation following Sutton Barto 4.3
             Against rush opponent, with afterstates
          """
          if self.read_path:
               policy_1, i_epoch = pickle.load(open(self.read_path, 'rb'))
          else:
               policy_1 = TabularPolicy()
               i_epoch = 0
          policy_2 = TabularPolicy()
          
          theta = 0.01
          t = time.time()
          while True:
               delta = 0
               for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
                    v = policy_1.v_dict[num]
                    s = State(from_base10 = num)  # here s is afterstate
                    
                    # terminal state, v function equals game result (no reward for transition)
                    if s.is_terminal():
                         policy_1.v_dict[num] = s.get_reward()
                    else:
                         # non-terminal afterstates
                         opponent_afterstate = State(from_base10 = policy_2.move_dict[num])
                         if opponent_afterstate.is_terminal():
                             policy_1.v_dict[num] = opponent_afterstate.get_reward()
                         else:
                             policy_1.v_dict[num] = policy_1.v_dict[opponent_afterstate.get_num()]

                    delta = max(delta, np.abs(v - policy_1.v_dict[num]))
               
               i_epoch += 1
               
               if delta < theta:
                    print('Value function has converged!')
                    print("Trained %i epochs so far." % i_epoch)
                    pickle.dump((policy_1, i_epoch), open(self.write_path, "wb" ) )
                    break
               
               if time.time() - t > 10:
                    t = time.time()
                    print("Trained %i epochs so far." % i_epoch)
                    pickle.dump((policy_1, i_epoch), open(self.write_path, "wb" ) )
     
     def PolicyImprovement(self):
          """ Policy Improvement following Sutton Barto 4.3
              Against rush opponent, with afterstates
          """
          policy_stable = True
          for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
               s = State(from_base10 = num)
               if not s.is_terminal():
                    old_action_num = policy_1.move_dict[num]
                    # get the best afterstates
                    
               
if __name__ == '__main__':
#     Train(read_path = r'C:\Users\daugh\Documents\GitHub\rl_tictactoe_data\policy_evaluation.pkl', write_path = r'C:\Users\daugh\Documents\GitHub\rl_tictactoe_data\policy_evaluation.pkl')               
     Train(write_path = os.path.dirname(os.getcwd()) + '/policy_evaluation.pkl')               