from tkinter import Tk, Button, messagebox
from tkinter.font import Font
import itertools
import numpy as np
import ttt_policies

class State:
    
    def __init__(self, board=[[0,0,0],[0,0,0],[0,0,0]], turn = 1, from_base10 = None):
        """
        Input:
            board: 0 for empty, 1 and 2 for players 1 and 2
            turn:  1 or 2, denoting who should make the next move
        """
        if not from_base10:
             self.board = board
             self.turn = turn
        else:
             num_str = np.base_repr(from_base10, base = 3)
             if len(num_str) != 10:  # expect 1 digit for turn and 9 for board
                  raise ValueError('Bad numerical representation of board: %s.' % num_str)
             self.turn = int(num_str[0])
             self.board = [
                       [int(num_str[1]), int(num_str[2]), int(num_str[3])],
                       [int(num_str[4]), int(num_str[5]), int(num_str[6])],
                       [int(num_str[7]), int(num_str[8]), int(num_str[9])]
                       ]             
        
    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
           
    def get_num(self):
        num_str= str(self.turn)
        for s in itertools.chain.from_iterable(self.board):
             num_str += str(s)
        return int(num_str, 3)
   
    def judge(self):
        """
        Returns:
             1 or 2 if player 1 or 2 wins. -1 for unfinished game. 0 for tie.
        Assumes at most one player wins. Output is arbitrary if both players have a row/column/diagonal, which should not arise in a real game.
        It is intentional that this method is separated from the Engine methods to compute rewards.
        """
        # horizontal
        for r in range(3):
             if self.board[r] == [1, 1, 1]:
                  return 1
             elif self.board[r] == [2, 2, 2]:
                  return 2
        # vertical
        for c in range(3):
             if self.board[0][c] == self.board[1][c] == self.board[2][c] and self.board[0][c] != 0:
                  return self.board[0][c]
        # diagonal
        x = self.board[1][1]
        if x != 0:
             if self.board[0][0] == x == self.board[2][2]:
                  return x
             if self.board[0][2] == x == self.board[2][0]:
                  return x
        # tied
        if (0 not in self.board[0]) and (0 not in self.board[1]) and (0 not in self.board[2]):
             return 0
        return -1  

class Action:
     
     def __init__(self, state: State, move: (int, int)):
          """
          Input:
               state: the state from which the action is taken
               move: the grid on which to place a move
          """
          self.state = state
          self.move = move
          
     def is_legal(self):
          return self.state.board[self.move[0]][self.move[1]] == 0
          
     def next_state(self):
          self.state.board[self.move[0]][self.move[1]] = self.state.turn
          self.state.change_turn()
          return self.state

class Game():
     def __init__(self):
          self.state = State()
          self.policy = ttt_policies.RushPolicy()

     def computer_move(self):
         """ Move by the computer player, following policy
         """
         action = self.policy.select_move(self.state)
         self.state = action.next_state()

     def judge(self):
        """
        Returns:
             1 or 2 if player 1 or 2 wins. -1 for unfinished game. 0 for tie.
        Assumes at most one player wins. Output is arbitrary if both players have a row/column/diagonal, which should not arise in a real game.
        It is intentional that this method is separated from the Engine methods to compute rewards.
        """
        return self.state.judge()         
    
class GUIGame(Game):
    def __init__(self):
        super().__init__()
        self.app = Tk()
        self.app.title('TicTacToe')
        self.app.resizable(width=False, height=False)
        self.font = Font(family="Helvetica", size=32)
        self.exit_flag = 0
        self.buttons = {}
        for x in range(3):
             for y in range(3):
                  handler = lambda x=x,y=y: self.human_move(x,y).computer_move()
                  button = Button(self.app, command=handler, font=self.font, width=2, height=1)
                  button.grid(row=y, column=x)
                  self.buttons[x,y] = button
        
    def human_move(self, x, y):
         """ Move by the human player
         Input:
              x, y: coordinates of the move.
         """
         self.app.update()
         action = Action(self.state, (x, y))
         if action.is_legal():
              self.state = action.next_state()
         self.update()
         return self
         
    def computer_move(self):
         """ Move by the computer player, following policy
         """
         if not self.exit_flag:
              super().computer_move()
              self.update()

    def update(self):
         for x in range(3):
              for y in range(3):
                   if self.state.board[x][y] == 1:
                        text = "X"
                   elif self.state.board[x][y] == 2:
                        text = "O"
                   else:
                        text = ""
                   self.buttons[x,y]['text'] = text
                   self.buttons[x,y]['disabledforeground'] = 'black'
                   if text=="":
                        self.buttons[x,y]['state'] = 'normal'
                   else:
                        self.buttons[x,y]['state'] = 'disabled'
                   self.buttons[x,y].update()
          
         game_result = self.judge()  
         if game_result == 1:
               messagebox.showinfo("Game Finished", "Player wins")
               self.exit_flag = 1
               self.app.destroy()
               print('done')
         elif game_result == 2:
               messagebox.showinfo("Game Finished", "Computer wins")
               self.exit_flag = 1
               self.app.destroy()
               print('done')
         elif game_result == 0:
              messagebox.showinfo("Game Finished", "Tied")
              self.exit_flag = 1
              self.app.destroy()
              print('done')
        

    
    def mainloop(self):
         self.app.mainloop()

if __name__ == '__main__':
     GUIGame().mainloop()
