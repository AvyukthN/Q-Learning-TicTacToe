import numpy as np

class Board():
    def __init__(self, p1, p2, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((self.rows, self.cols))

        self.p1 = p1
        self.p2 = p2
        self.playerMoving = 1

        self.board_hash = None
    
    def update_board(self, coords):
        self.board[coords[0]][coords[1]]

    def get_open_positions(self):
        positions = []

        for i in range(len(self.board)):
            for j in range(len(self.board[j])):
                if self.board[i][j] == 0:
                    positions.append((i, j)) # (row, col)

        return positions

    def get_board_hash(self):
        self.board_hash = self.board.reshape(self.rows * self.cols)

        return self.board_hash