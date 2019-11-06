# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 22:09:24 2019

@author: josephwang
"""
from tkinter import Tk, Button
from tkinter.font import Font
import random

class State:
    
    def __init__(self, board=[[0,0,0],[0,0,0],[0,0,0]], turn = 1):
        """
        Input:
            board: 0 for empty, 1 and 2 for players 1 and 2
            turn:  1 or 2, denoting who should make the next move
        """
        self.board = board
        self.turn = turn
        
    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

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
        
class Engine:
    """
    For now, a random move engine. Will be expanded.
    """
    def move(self, state):
        """
        Input:
            state: the current state
        Returns:
            A state, in which a move has been made
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
        position = random.choice(legal_positions)
        state.board[position[0]][position[1]] = state.turn
        state.change_turn()
        return state
    
class Game:
    def __init__(self):
        self.state = State()
                  
    def judge(self):
        """
        Returns:
             1 or 2 if player 1 or 2 wins. -1 for unfinished game. 0 for tie.
        Assumes at most one player wins. Output is arbitrary if both players have a row/column/diagonal, which should not arise in a real game.
        It is intentional that this method is separated from the Engine methods to compute rewards.
        """
        # horizontal
        for r in range(3):
             if self.state.board[r] == [1, 1, 1]:
                  return 1
             elif self.state.board[r] == [2, 2, 2]:
                  return 2
        # vertical
        for c in range(3):
             if self.state.board[0][c] == self.state.board[1][c] == self.state.board[2][c] and self.state.board[0][c] != 0:
                  return self.state.board[0][c]
        # diagonal
        x = self.state.board[1][1]
        if x != 0:
             if self.state.board[0][0] == x == self.state.board[2][2]:
                  return x
        # tied
        if (0 not in self.state.board[0]) and (0 not in self.state.board[1]) and (0 not in self.state.board[2]):
             return 0
        return -1

#class GUI:
#
#  def __init__(self):
#    self.app = Tk()
#    self.app.title('TicTacToe')
#    self.app.resizable(width=False, height=False)
#    self.game = Game()
#    self.font = Font(family="Helvetica", size=32)
#    self.buttons = {}
#
#    for x in range(3):
#       for y in range(3):
#           handler = lambda x=x,y=y: self.move(x,y)
#           button = Button(self.app, command=handler, font=self.font, width=2, height=1)
#           button.grid(row=y, column=x)
#           self.buttons[x,y] = button
#    handler = lambda: self.reset()
#    button = Button(self.app, text='reset', command=handler)
#    button.grid(row=self.board.size+1, column=0, columnspan=self.board.size, sticky="WE")
#    handler = lambda: None
#    button = Button(self.app, text='dummy', command=handler)
#    button.grid(row=self.board.size+2, column=0, columnspan=self.board.size, sticky="WE")
#    self.update()