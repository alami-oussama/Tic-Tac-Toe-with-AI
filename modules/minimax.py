import numpy as np
from .game import is_available, is_completed, is_winner

def minimax(board, maximizing):
    if is_winner(board, 2):
        return 1

    if is_winner(board, 1):
        return -1

    if is_completed(board):
        return 0
    
    if maximizing:
        max_score = -np.inf
        for row in range(3):
            for col in range(3):
                position = (col, row)
                if is_available(board, position):
                    board[row][col] = 2
                    score = minimax(board, False)
                    board[row][col] = 0
                    max_score = max(score, max_score)
        return max_score
    
    if not maximizing:
        min_score = np.inf
        for row in range(3):
            for col in range(3):
                position = (col, row)
                if is_available(board, position):
                    board[row][col] = 1
                    score = minimax(board, True)
                    board[row][col] = 0
                    min_score = min(score, min_score)
        return min_score

def best_move(board):
    best_score = -np.inf
    for row in range(3):
        for col in range(3):
            position = (col, row)
            if is_available(board, position):
                board[row][col] = 2
                score = minimax(board, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = position

    col, row = move
    board[row][col] = 2
    return move