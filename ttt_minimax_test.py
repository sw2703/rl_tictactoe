# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 09:39:13 2019

@author: daugh
"""

from ttt_minimax import Board

def test_opponent_wins_horizontal():
    board = Board()
    for x in range(board.size):
        board.fields[x, 0] = board.opponent
    assert board.won()
    
def test_opponent_wins_vertical():
    board = Board()
    for y in range(board.size):
        board.fields[y, 0] = board.opponent
    assert board.won()
    
def test_opponent_wins_diagonals():
    board = Board()
    for i in range(board.size):
        board.fields[i, i] = board.opponent
    assert board.won()
    for i in range(board.size):
        board.fields[i, board.size-i] = board.opponent
    assert board.won()