import settings
import random
random.seed(settings.SEED)
import torch
from torch import nn
torch.manual_seed(settings.SEED)
import numpy as np
np.random.seed(settings.SEED)
from collections import deque
from model import Linear_QNet, QTrainer

from creature import Plant, Prey, Hunter, Seed



class Agent:

    def __init__(self, simulation, hosttype):
        self.simulation = simulation
        self.hosttype = hosttype
        self.n_games = 0

        if hosttype == Prey:
            stats = settings.generate_prey_heritage_stats()
            self.vision_radius = stats["vision_radius"]
            self.lr = stats["lr"]
            self.gamma = stats["gamma"]
            self.batch_size = stats["batch_size"]
            self.epsilon_decay = stats["epsilon_decay"]
            self.min_epsilon = stats["min_epsilon"]
            self.max_memory = stats["max_memory"]

        elif hosttype == Hunter:
            stats = settings.generate_hunter_heritage_stats()
            self.vision_radius = stats["vision_radius"]
            self.lr = stats["lr"]
            self.gamma = stats["gamma"]
            self.batch_size = stats["batch_size"]
            self.epsilon_decay = stats["epsilon_decay"]
            self.min_epsilon = stats["min_epsilon"]
            self.max_memory = stats["max_memory"]

            
        self.memory = deque(maxlen=self.max_memory) # popleft()
        self.model = Linear_QNet((2*self.vision_radius+1)**2, 256, 128, 64, 8).to(settings.DEVICE)
        # self.model = Linear_QNet(8, 256, 8).cuda()
        self.trainer = QTrainer(self.model, self.lr, self.gamma)

        self.epsilon = 1



    def get_state(self, danger_matrix):
        state = danger_matrix.flatten() 
        return state       
        #return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > self.batch_size:
            mini_sample = random.sample(self.memory, self.batch_size) # list of tuples
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):

        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.min_epsilon, self.epsilon)
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
    exec(open("main.py").read())