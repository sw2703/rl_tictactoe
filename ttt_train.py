from ttt_play import Game
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
          """Policy Iteration following Sutton Barto 4.3
          """
          # 1. Initialization
          policy_1 = TabularPolicy(has_v_dict = True)
          policy_2 = TabularPolicy(has_v_dict = True)
          
          # 2. Policy Evaluation
          delta = 0
          for _ in range(n_game):
               