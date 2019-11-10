import numpy as np
import random
import pickle
import time
import ttt_play

class Policy:
    """ By default, a random policy. Other policies are children of this class.
    """
    def select_move(self, state):
        """
        Input:
            state: the current state
        Returns:
            An action
        Raises:
            RuntimeError, if the board has already been filled
        """
        legal_positions = []
        for x in range(3):
            for y in range(3):
                if state.board[x][y] == 0:
                    legal_positions.append((x,y))
        if not legal_positions:
            raise RuntimeError('Cannot make a move on a full board!')
        move = random.choice(legal_positions)
        return ttt_play.Action(state, move)

class SlowRandomPolicy(Policy):
    """ Random policy with a time delay
    Input: 
        delay: seconds to delay for each move.
    """
    def __init__(self, delay):
         self.delay = delay
    
    def select_move(self, state):
        time.sleep(self.delay)
        return super().select_move(state)

class TabularPolicy(Policy):
     """ Use a dictionary to store the action chosen from each state.
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
                    self.v_dict[state.get_tuple()] = 0
               try:
                    self.move_dict[state.get_tuple()] = self.rush_move(state)
               except(RuntimeError):
                    pass
               
               state = ttt_play.State(board, turn = 2)
               if self.has_v_dict:
                    self.v_dict[state.get_tuple()] = 0
               try:
                    self.move_dict[state.get_tuple()] = self.rush_move(state)
               except(RuntimeError):
                    pass
          
     def rush_move(self, state):
          for x in range(3):
                 for y in range(3):
                     if state.board[x][y] == 0:
                          return ttt_play.Action(state, (x, y))
          raise RuntimeError('Cannot make a move on a full board!')
          
     def store_dict(self, path):
          pickle.dump(self.move_dict, open(path, 'wb'))
          
     def read_dict(self, path):
          try: 
               self.move_dict = pickle.load(open(path, 'rb'))
          except:
               raise RuntimeError('The saved mvoe_dict cannot be read. Using default dict instead.')

class RushPolicy(TabularPolicy):
     """ Always selects the first available action.
     """          
     def select_move(self, state):
          action = self.move_dict[state.get_tuple()]
          return action    

          