import ttt_play
from copy import deepcopy

class TabularPolicy():
     """ By default, a rush policy, i.e. selects the first available move.
     """
     def __init__(self):
          self.init_v_dict()
          self.init_move_dict()
     
     
     def init_v_dict(self):
          self.v_dict = dict()
          for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
               self.v_dict[num] = 0
     
     
     def init_move_dict(self):
          self.move_dict = dict()
          for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
               state = ttt_play.State(from_base10 = num)
               try:
                    self.move_dict[state.get_num()] = self.rush_move(state)
               except(RuntimeError):
                    pass
     
     
     def rush_move(self, state):
          out_state = deepcopy(state)
          for x in range(3):
                 for y in range(3):
                     if out_state.board[x][y] == 0:
                          out_state.board[x][y] = state.turn
                          out_state.change_turn()
                          return out_state
          raise RuntimeError('Cannot make a move on a full board!') 
          
     
     def after_state(self, state):
          return self.move_dict[state.get_num()]