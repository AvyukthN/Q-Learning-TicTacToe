import pandas as pd

class Board:
    def __init__(self, game_id, num_rows=3, num_columns=3):
        self.rows = num_rows
        self.cols = num_columns
        self.game_id = game_id
        # self.board = [[0 for i in range(self.cols)] for i in range(self.rows)]
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        self.player_hash = {'X': 2, 'O': 1, ' ': 0}
        self.piece_hash = {value: key for key, value in self.player_hash.items()}
        self.prev_states = []
    
    def make_move(self, player, move):
        legal_moves = self.get_legal_moves()

        if move in legal_moves:
            self.board[move[0]][move[1]] = self.player_hash[player]
            self.prev_states.append(self.get_board_hash())
            # self.prev_states.update({self.get_board_hash(): move})

    def check_win(self):
        for i in range(len(self.board)):
            row_count = 0
            for j in range(1, len(self.board[i])):
                if self.board[i][j] == self.board[i][j-1] and self.board[i][j] != 0:
                    row_count += 1
            
                if row_count == 2:
                    self.record_game(self.board[i][j])
                    return self.board[i][j]
        
        for i in range(len(self.board)):
            col_count = 0
            for j in range(1, len(self.board[i])):
                if self.board[j][i] == self.board[j-1][i] and self.board[j][i] != 0:
                    col_count += 1
            
                if col_count == 2:
                    self.record_game(self.board[j][i])
                    return self.board[j][i]

        # FOR DIAGONALS ON 3x3 BOARD
        diag1 = [(0, 0), (1, 1), (2, 2)]
        diag2 = [(2, 0), (1, 1), (0, 2)]

        diag1 = [self.board[coord[0]][coord[1]] for coord in diag1]
        diag2 = [self.board[coord[0]][coord[1]] for coord in diag2]
        
        diag_count = 0
        for i in range(1, len(diag1)):
            if diag1[i] == diag1[i-1] and diag1[i] != 0:
                diag_count += 1
        
            if diag_count == 2:
                self.record_game(diag1[i])
                return diag1[i] 
        
        diag_count = 0
        for i in range(1, len(diag2)):
            if diag2[i] == diag2[i-1] and diag2[i] != 0:
                diag_count += 1

            if diag_count == 2:
                self.record_game(diag2[i])
                return diag2[i]

        return False
    
    def check_tie(self):
        board_markers = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                board_markers.append(self.board[i][j])
        
        if 0 not in board_markers:
            return True
        return False

    
    def record_game(self, winner):
        game_hash = {
            'game_id': [self.game_id],
            'winner': [winner]
        }

        if len(self.prev_states) != 9:
            for i in range(9 - len(self.prev_states)):
                self.prev_states.append('0')

        for i in range(len(self.prev_states)):
            game_hash.update({'state-{}'.format(str(i+1)): pd.Series([self.prev_states[i]])})
        
        df = pd.read_csv('./game_data/games.csv', index_col=False)
        df = df.to_dict()
        df.pop("Unnamed: 0")

        final_df = {
            'id': None,
            'winner': None,
            'state-1': None, 
            'state-2': None, 
            'state-3': None, 
            'state-4': None, 
            'state-5': None, 
            'state-6': None, 
            'state-7': None, 
            'state-8': None, 
            'state-9': None, 
        }

        df_vals = [list(val.values()) for key, val in df.items()]
        df2_vals = [list(val) for key, val in game_hash.items()]
        final_df_keys = list(final_df.keys())

        final_df_vals = []
        for i in range(len(df_vals)):
            temp_arr = df_vals[i] + df2_vals[i]
            final_df_vals.append(temp_arr)

        for i in range(len(final_df_vals)):
            final_df.update({final_df_keys[i]: pd.Series(final_df_vals[i])})
        
        pd.DataFrame(final_df).to_csv('./game_data/games.csv')

    def get_legal_moves(self):
        legal_moves = []

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    legal_moves.append((i, j)) # (row, col)
        
        return legal_moves
    
    def get_board_hash(self):
        hashed = '/'.join([''.join([str(elem) for elem in row]) for row in self.board])

        return hashed
    
    def print_board(self):
        final_str = '+---+---+---+\n'
        for i in range(len(self.board)):
            temp_str = '| '
            for j in range(len(self.board[i])):
                piece = self.piece_hash[self.board[i][j]]
                temp_str += piece + ' | '
            temp_str += '\n+---+---+---+\n'

            final_str += temp_str
        
        print(final_str)

    def clear_board(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]