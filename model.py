import settings
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
torch.manual_seed(settings.SEED)
import os
import numpy as np
np.random.seed(settings.SEED)
from datetime import datetime
from creature import Plant, Prey, Hunter, Seed

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size_1, hidden_size_2, hidden_size_3, output_size):
        super().__init__()
        # definiert die Struktur des neuronalen Netzwerks 
        self.linear1 = nn.Linear(input_size, hidden_size_1)
        self.linear2 = nn.Linear(hidden_size_1, hidden_size_2)
        self.linear3 = nn.Linear(hidden_size_2, hidden_size_3)
        self.linear4 = nn.Linear(hidden_size_3, output_size)

        
    def forward(self, x):     
        # Kernfunktion des NN, Gegenspieler zu Backpropagation   
        x = x.to(settings.DEVICE)
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = F.relu(self.linear3(x))
        x = self.linear4(x)
        return x

    def save(self): 
        # delete all files in model folder       
        model_folder_path = './model'
        for file in [f for f in os.listdir(model_folder_path)]:
            #print(_)
            os.remove(model_folder_path + '/' + file)
        now = datetime.now()
        file_name = f'{now.strftime("%Y%m%d_%H%M%S")}.pth'

        # save the latest model 
        print(file_name)
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

    def load(self):
        model_folder_path = './model'
        file_name = os.path.join(model_folder_path, os.listdir(model_folder_path)[0])
        
        self.load_state_dict(torch.load(file_name))
        self.eval()

class QTrainer:
    def __init__(self, model, lr, gamma):
        
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(np.array(state), dtype=torch.float, device=settings.DEVICE)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float, device=settings.DEVICE)
        action = torch.tensor(np.array(action), dtype=torch.long, device=settings.DEVICE)
        reward = torch.tensor(np.array(reward), dtype=torch.float, device=settings.DEVICE)
        done = torch.tensor(np.array(done), dtype=torch.bool, device=settings.DEVICE)

        if len(state.shape) == 1:
            state, next_state, action, reward, done = [t.unsqueeze(0) for t in [state, next_state, action, reward, done]]

        # Vorhersage für aktuellen Zustand
        pred = self.model(state)

        # Zielwerte initialisieren
        target = pred.clone()

        # Berechne Q-Werte effizienter
        with torch.no_grad():
            max_next_Q = torch.max(self.model(next_state), dim=1)[0]
            Q_new = reward + (self.gamma * max_next_Q * ~done)

        # Aktualisiere nur die Werte für die getätigten Aktionen
        target[range(len(action)), action.argmax(dim=1)] = Q_new

        # Backpropagation
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()



if __name__ == "__main__":
    exec(open("main.py").read())
