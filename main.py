from board import Board
from agent import Agent
import random

def main():
    q_agent = Agent()
    win = False
    p1 = True

    for i in range(255168):
        b = Board(1)
        while True:
            if p1:
                b.print_board()

                q_agent.update_q_value(b, mode="inference")
                # b.make_move('X', (int(move[0]), int(move[1])))
                
                win = b.check_win()
                tie = b.check_tie()
                if win or tie:
                    b.print_board()
                    break
                p1 = False
            else:
                b.print_board()

                move = input('Player ')
                move = move.split()
                '''
                legal_moves = b.get_legal_moves()
                rand_index = random.randint(0, len(legal_moves) - 1)
                move = legal_moves[rand_index]
                '''

                b.make_move('O', (int(move[0]), int(move[1])))

                win = b.check_win()
                tie = b.check_tie()
                if win or tie:
                    b.print_board()
                    break
                p1 = True

    '''
    with open('q-table.txt', 'w') as f:
        f.write(str(q_agent.q_table))    
    '''

if __name__ == '__main__':
    main()