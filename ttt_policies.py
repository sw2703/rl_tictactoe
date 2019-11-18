import numpy as np
import pickle
import ttt_play


class TabularPolicy():
     """ By default, a rush policy, i.e. selects the first available move.
     """
     def __init__(self, has_v_dict = False):
          self.has_v_dict = has_v_dict
          if self.has_v_dict:
               self.v_dict = dict()
          self.move_dict = dict()
          for i in range(3**9):
               num_str = np.base_repr(i, base = 3)
               num_str = '0' * (9 - len(num_str)) + num_str
               board = [
                         [int(num_str[0]), int(num_str[1]), int(num_str[2])],
                         [int(num_str[3]), int(num_str[4]), int(num_str[5])],
                         [int(num_str[6]), int(num_str[7]), int(num_str[8])]
                         ]
               
               state = ttt_play.State(board, turn = 1)
               if self.has_v_dict:
                    self.v_dict[state.get_num()] = 0
               try:
                    self.move_dict[state.get_num()] = self.rush_move(state)
               except(RuntimeError):
                    pass
               
               state = ttt_play.State(board, turn = 2)
               if self.has_v_dict:
                    self.v_dict[state.get_num()] = 0
               try:
                    self.move_dict[state.get_num()] = self.rush_move(state)
               except(RuntimeError):
                    pass
          
     def rush_move(self, state):
          for x in range(3):
                 for y in range(3):
                     if state.board[x][y] == 0:
                          return ttt_play.Action(state, (x, y))
          raise RuntimeError('Cannot make a move on a full board!')
     
     
     def select_move(self, state):
          return self.move_dict[state.get_num()]
     
     
     def store_dict(self, path):
          pickle.dump(self.move_dict, open(path, 'wb'))
          
          
     def read_dict(self, path):
          try: 
               self.move_dict = pickle.load(open(path, 'rb'))
          except:
               raise RuntimeError('The saved mvoe_dict cannot be read. Using default dict instead.')

          