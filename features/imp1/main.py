from board import Board

if __name__ == '__main__':
    board = Board('avy', 'computer')

    board_hash = board.get_board_hash()

    print(board_hash)