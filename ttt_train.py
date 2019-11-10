from ttt_play import Game, State
from ttt_policies import Policy, TabularPolicy

class Train:
     def __init__(self, n_game, read_path = None, write_path):
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
          for _ in range(n_game):
               delta = 0
               for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
                    v = policy_1.v_dict[num]
                    s = State(from_base10 = num)
                    opponent_state = policy_1.select_move(s).next_state()
                    if 
                    s_prime = policy_2.select_move(opponent_state).next_state()
                    policy_1.v_dict[num] = 
                    