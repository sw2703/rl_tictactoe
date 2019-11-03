# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 22:09:24 2019

@author: daugh
"""

class State:
    
    def __init__(self, board=[[0,0,0],[0,0,0],[0,0,0]], turn = 1):
        """
        Input:
            board: 0 for empty, 1 and 2 for players 1 and 2
            turn:  1 or 2, denoting who should make the next move
        """
        self.board = board
        self.turn = turn
        
    