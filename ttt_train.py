from ttt_play import State
from ttt_policies import TabularPolicy, RushPolicy
import numpy as np
import pickle
import time

class Train:
     def __init__(self, n_game, write_path, read_path = None):
          """
          Input:
               n_game: number of games to train for
               read_path, write_path: paths for reading or saving the model
          """
          self.n_game = n_game
          self.read_path = read_path
          self.write_path = write_path
          self.SelfPlay()
               
     def SelfPlay(self):
          """Policy Evaluation following Sutton Barto 4.1
             Against rush opponent
             with regular states, no afterstates
          """
          policy_1 = TabularPolicy(has_v_dict = True)
          policy_2 = RushPolicy()
          
          theta = 0.01
          t = time.time()
          for i_game in range(self.n_game):
               delta = 0
               for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
                    v = policy_1.v_dict[num]
                    s = State(from_base10 = num)
                    
                    # terminal state, v function always zero
                    if s.is_terminal():
                         policy_1.v_dict[num] = 0
                         continue
                    
                    opponent_state = policy_1.select_move(s).next_state()
                    r = opponent_state.get_reward()
                    if opponent_state.is_terminal():
                         v_s_prime = 0
                    else:
                         s_prime = policy_2.select_move(opponent_state).next_state()
                         v_s_prime = policy_1.v_dict[s_prime.get_num()]
                              
                    policy_1.v_dict[num] = r + v_s_prime
                    delta = max(delta, np.abs(v - policy_1.v_dict[num]))
                    
               if delta < theta:
                    break
               
               if time.time() - t > 60:
                    t = time.time()
                    print("Trained %i games so far." % i_game)
                    pickle.dump(policy_1, open(self.write_path, "wb" ) )
               
if __name__ == '__main__':
     Train(n_game = 1000, write_path = r'C:\Users\daugh\Documents\GitHub\rl_tictactoe\policy_evaluation.pkl')               