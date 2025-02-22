import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
import settings



class Agent:

    def __init__(self, simulation):
        self.simulation = simulation
        self.n_games = 0
        self.memory = deque(maxlen=settings.MAX_MEMORY) # popleft()
        self.model = Linear_QNet(4, 256, 8)
        # self.model = Linear_QNet(8, 256, 8).cuda()
        self.trainer = QTrainer(self.model, lr=settings.LR, gamma=settings.GAMMA)

        self.epsilon = 1



    def get_state(self, akteur, target):
        if target != 0:
            state = [
                    akteur.pos[0],
                    akteur.pos[1],
                    target.pos[0],
                    target.pos[1],
                    # 1 if akteur.pos[0] == 0 else (settings.GRID_WIDTH-1 - akteur.pos[0]+1)/(settings.GRID_WIDTH),
                    # 1 if akteur.pos[0] == (settings.GRID_WIDTH-1) else (akteur.pos[0]+1)/(settings.GRID_WIDTH),

                    # 1 if akteur.pos[1] == 0 else (settings.GRID_HEIGHT-1 - akteur.pos[1]+1)/(settings.GRID_HEIGHT),
                    # 1 if akteur.pos[1] == (settings.GRID_HEIGHT-1) else (akteur.pos[1]+1)/(settings.GRID_HEIGHT),

                    # 1 if akteur.pos[0] < target.pos[0] else 0,
                    # 1 if akteur.pos[0] > target.pos[0] else 0,
                    # 1 if akteur.pos[1] < target.pos[1] else 0,
                    # 1 if akteur.pos[1] > target.pos[1] else 0,
                    ]
        else:
            state = [0,0,0,0]

        return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > settings.BATCH_SIZE:
            mini_sample = random.sample(self.memory, settings.BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):

        self.epsilon *= settings.EPSILON_DECAY
        self.epsilon = max(settings.MIN_EPSILON, self.epsilon)
        final_move = [0,0,0,0,0,0,0,0]

        if random.random() < self.epsilon:
            move = random.randint(0, 7)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1


        return final_move


if __name__ == "__main__":
    exec(open("simulation.py").read())
