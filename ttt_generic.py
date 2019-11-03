# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 22:09:24 2019

@author: daugh
"""

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