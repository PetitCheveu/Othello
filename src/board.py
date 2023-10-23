def init_board():
    board = [['_' for _ in range(8)] for _ in range(8)]
    board[3][3], board[4][4] = 'W', 'W'
    board[3][4], board[4][3] = 'B', 'B'
    return board
