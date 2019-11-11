from ttt_play import State
from ttt_policies import TabularPolicy, RushPolicy
import numpy as np

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
          for _ in range(self.n_game):
               delta = 0
               for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
                    v = policy_1.v_dict[num]
                    s = State(from_base10 = num)
                    r = s.get_reward()
                    if r == 0:
                         opponent_state = policy_1.select_move(s).next_state()
                         r = opponent_state.get_reward()
                         if r == 0:
                              s_prime = policy_2.select_move(opponent_state).next_state()
                              if s_prime.judge() == 2:
                                   r = -1
                              else:
                                   r = 0
                              
                    policy_1.v_dict[num] = r + policy_1.v_dict[s_prime.get_num()]
                    delta = max(delta, np.abs(v - policy_1.v_dict[num]))
                    
               if delta < theta:
                    break
               
if __name__ == '__main__':
     Train(n_game = 1, write_path = r'C:\Users\daugh\Documents\GitHub\rl_tictactoe\policy_evaluation.pkl')               