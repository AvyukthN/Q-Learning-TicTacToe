from board import State
from board import Agent

if __name__ == '__main__':
    rl_agent = Agent()
    rl_agent.play(rounds=100000)