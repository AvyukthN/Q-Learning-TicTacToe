import numpy as np

class State:
    def __init__(self, width=4, height=3, start=(2, 0), win=(0, 3), lose=(1, 3)):
        self.w = width
        self.h = height
        self.starting_state = start
        self.winning_state = win
        self.losing_state = lose
        self.finished = False
        
        self.current_state = start

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
        if self.board[move[0]][move[1]] == -1:
            return False
        if (move[0] <= self.height - 1) and (move[0] >= 0):
            if (move[1] <= self.l - 1) and (move[0] >= 0):
                return True
    
    def get_next_position(self, action):
        curr_pos = self.current_state
        if self.actions[action] == 0:
            # up
            next_pos = (curr_pos[0] - 1, curr_pos[1])
        elif self.actions[action] == 1:
            # down 
            next_pos = (curr_pos[0] + 1, curr_pos[1])
        elif self.actions[action] == 2:
            # left
            next_pos = (curr_pos[0], curr_pos[1] - 1)
        elif self.actions[action] == 3:
            # right 
            next_pos = (curr_pos[0] - 1, curr_pos[1] + 1)
        
        if self.move_legality(self, next_pos):
            return next_pos

        return self.current_state

class Agent:
    def __init__(self):
        self.states = []
        self.actions = ['up', 'down', 'left', 'right']
        self.state = State()
        self.lr = 0.2
        self.exp_rate = 0.3

        # initialize state values for board
        self.state_values = {}
        for i in range(self.state.w):
            for j in range(self.state.h):
                self.state_values.update({(i, j): 0})
    
    def optimize_action(self):
        # have to choose the action with the highest estimated state value V(St)
        min_next_reward = 0
        action = ""

        if np.random.uniform(0, 1) < self.exp_rate:
            action = self.actions[np.random(0, len(self.actions) - 1)]
        else:
            # greedy heuristic that picks best estimated V(St) based on rewards that were backpropogated
            # iterate through the values found for each next state that occurs for each action
            for board_action in self.actions:
                next_reward = self.state_values[self.state.get_next_position(board_action)]
                if next_reward > min_next_reward:
                    action = board_action
                    min_next_reward = next_reward
        
        return action

    def play(self, rounds=10):
        for i in range(len(rounds)):
            if self.state.finished:
                # backpropogate through board and update estimated state values
                reward = self.state.get_reward()

                self.state_values.update({self.state.current_state: reward})
                print('updated V(St) {}'.format(reward))
            
                for board_state in reversed(self.states):
                    # value iteration function
                    reward = self.state_values[board_state] + (self.lr * (reward - self.state_value[board_state]))
                    self.state_values[board_state] = round(reward, 3)

                self.reset()
            else:
                action = self.optimize_action()

                # append state
                self.states.append(self.state.get_next_position(action))
                # print policy decision
                print("Policy Function")
                print("")

        
    def reset(self):
        self.states = []
        self.state = State()
