def mark_square(board, position, player):
    col, row = position
    board[row][col] = player

def is_available(board, position):
    col, row = position
    return 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == 0

def is_completed(board):
    for row in range(3):
        for col in range(3):
            if is_available(board, (col, row)):
                return False
    return True

def is_winner(board, player):
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True

    # Check the main diagonal
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True

    # Check the secondary diagonal
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False