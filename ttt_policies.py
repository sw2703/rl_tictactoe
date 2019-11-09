import random
import time
import ttt_generic

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
        return ttt_generic.Action(state, move)

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
