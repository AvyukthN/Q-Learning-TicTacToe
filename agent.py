class Agent:
    def __init__(self, q_table={}):
        self.q_table = q_table # {board_pos: [all legal_moves]}
        self.discount_rate = 0.9
        self.lr = 0.1
        self.mode = "training"
    
    def update_q_value(self, board, mode="training"):
        if mode == "training":
            self.update_q_table(board)
            prev_board = board.get_board_hash()

            best_prev_move, best_prev_val = self.get_highest_q_val(prev_board)

            board.make_move('X', best_prev_move)
            self.update_q_table(board)

            best_curr_move, best_curr_val = self.get_highest_q_val(board.get_board_hash())

            reward = self.reward_function(board)
            temporal_diff = self.get_temporal_difference(reward, best_curr_val, best_prev_val)

            new_q_val = self.bellman_equation(best_prev_val, temporal_diff)

            self.q_table[prev_board][best_prev_move] = new_q_val
            # print(self.q_table)
        elif mode == "inference":
            from q_table import q_table
            board_hash = board.get_board_hash()
            if board_hash in q_table.keys():
                calculated_q_vals = q_table[board_hash]
                max_val = float('-inf')
                best_move = None
                for key, val in calculated_q_vals.items():
                    if val > max_val:
                        max_val = val
                        best_move = key
                board.make_move('X', best_move)

    def bellman_equation(self, prev_q_val, temporal_diff):
        new_q_val = prev_q_val + (self.lr * temporal_diff) 

        print('bellman output {}'.format(new_q_val))
        return new_q_val
    
    def get_temporal_difference(self, reward, curr_max_q_val, prev_max_q_val):
        td = ((reward + (self.discount_rate * curr_max_q_val)) - prev_max_q_val)

        print('temporal differnce {}'.format(td))
        return td

    def reward_function(self, board):
        outcome = board.check_win()

        if outcome != False:
            if board.piece_hash[outcome] == 'X':
                board.print_board()
                board.clear_board()
                return 1000
            if board.piece_hash[outcome] == 'O':
                board.print_board()
                board.clear_board()
                return -1000
        else:
            return 0
    
    def update_q_table(self, board):
        if board.get_board_hash() not in list(self.q_table.keys()):
            # initializing as 0 creates pessimistic agent
            win_bool = board.check_win()
            val = 0
            if win_bool:
                val = 1

            self.q_table.update({board.get_board_hash(): {move: val for move in board.get_legal_moves()}})
    
    def get_highest_q_val(self, board_hash):
        max_value = float('-inf')
        best_move = None
        for key, value in self.q_table[board_hash].items():
            if value > max_value:
                best_move = key
                max_value = value

        return best_move, max_value