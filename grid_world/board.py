import numpy as np
import os
import random
import time

class State:
    def __init__(self, width=4, height=3, start=(2, 0), win=(0, 3), lose=(1, 3), curr_state=(2, 0)):
        self.w = width
        self.h = height
        self.starting_state = start
        self.winning_state = win
        self.losing_state = lose
        self.finished = False
        
        self.current_state = curr_state

        self.board = np.zeros((self.h, self.w))
        self.board[1][1] = -1

        self.actions = {'up': 0, 'down': 1, 'left': 2, 'right': 3}

    def get_reward(self):
        if self.current_state == self.winning_state:
            return 1
        if self.current_state == self.losing_state:
            return -1
        
        return 0
    
    def move_legality(self, move):
        if (move[0] <= self.h - 1) and (move[0] >= 0):
            if (move[1] <= self.w - 1) and (move[0] >= 0):
                # if self.board[move[0]][move[1]] != -1:
                if move != self.starting_state:
                    if move != (1, 1):
                        return True
        
        return False
    
    def get_next_position(self, action):
        if self.actions[action] == 0:
            # up
            next_pos = (self.current_state[0] - 1, self.current_state[1])
        elif self.actions[action] == 1:
            # down 
            next_pos = (self.current_state[0] + 1, self.current_state[1])
        elif self.actions[action] == 2:
            # left
            next_pos = (self.current_state[0], self.current_state[1] - 1)
        elif self.actions[action] == 3:
            # right 
            next_pos = (self.current_state[0], self.current_state[1] + 1)
        
        if self.move_legality(next_pos):
            if next_pos[0] < 0 or next_pos[1] < 0:
                return self.current_state
            return next_pos

        return self.current_state
    
    def check_end(self):
        if (self.current_state == self.winning_state) or (self.current_state == self.losing_state):
            self.finished = True
    
    def display_board_state(self):
        final_str = ''
        for i in range(len(self.board)):
            temp = ''
            for j in range(len(self.board[i])):
                if self.board[i][j] == -1:
                    character = '#'
                if self.board[i][j] != -1:
                    character = '.'
                if (i, j) == self.current_state:
                    character = '$'

                temp += character + ' '
            
            final_str += temp + '\n'
        
        print(final_str)

class Agent:
    def __init__(self):
        self.states = []
        self.actions = ['up', 'down', 'left', 'right']
        self.state = State()
        self.lr = 0.2
        # exploration rate (the threshold for policy to use prefound path or explore for a new one)
        self.exp_rate = 0.3

        # initialize state values for board
        self.state_values = {}
        for i in range(self.state.h):
            for j in range(self.state.w):
                self.state_values.update({(i, j): 0})
    
    def optimize_action(self):
        # have to choose the action with the highest estimated state value V(St)
        min_next_reward = float('-inf')
        action = ""

        if np.random.uniform(0, 1) < self.exp_rate:
            # rand_index = random.randint(0, len(self.actions) - 1)
            # action = self.actions[rand_index]
            action = np.random.choice(self.actions)
        else:
            # greedy heuristic that picks best estimated V(St) based on rewards that were backpropogated
            # iterate through the values found for each next state that occurs for each action
            for board_action in self.actions:
                next_reward = self.state_values[self.state.get_next_position(board_action)]
                if next_reward > min_next_reward:
                    action = board_action
                    min_next_reward = next_reward
        return action
    
    def execute_action(self, action):
        position = self.state.get_next_position(action)

        return State(curr_state=position)
    
    def display_state_values(self):
        for i in range(0, self.state.h):
            print('----------------------------------')
            out = '| '
            for j in range(0, self.state.w):
                out += str(self.state_values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------')

    '''
    def display_state_values(self):
        final_str = ""
        for i in range(self.state.h):
            temp = "| "
            for j in range(self.state.w):
                value = self.state_values[(i, j)]
                temp = str(self.state_values[(i, j)]).ljust(6) + ' | '
            
            temp += '\n'
            final_str += temp
        
        print(final_str)
    '''
        
    def play(self, rounds=10):
        for i in range(rounds):
            if self.state.finished:
                # backpropogate through board and update estimated state values
                reward = self.state.get_reward()

                self.state_values.update({self.state.current_state: reward})
                print('updated V(St) {}'.format(reward))
            
                for board_state in reversed(self.states):
                    # value iteration function
                    reward = self.state_values[board_state] + (self.lr * (reward - self.state_values[board_state]))
                    self.state_values[board_state] = round(reward, 3)

                self.reset()
                
                os.system('cls')
                self.display_state_values()
                self.state.display_board_state()
                time.sleep(0.01)
            else:
                action = self.optimize_action()

                # append state
                self.states.append(self.state.get_next_position(action))
                # print policy decision
                print("Policy Function")
                print("state {} map -> {} action".format(self.state.current_state, action))

                # maybe do this
                # self.state = State(state = self.state.get_next_position(action))
                self.state = self.execute_action(action)

                self.state.check_end()

                os.system('cls')
                self.display_state_values()
                self.state.display_board_state()
                time.sleep(0.01)

    def reset(self):
        self.states = []
        self.state = State()
