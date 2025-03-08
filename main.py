import threading
from simulation import Simulation
from display import Display
from queue import Queue
import time


class App:
    def __init__(self):
        self.simulation = Simulation(self)
        self.all_data = []
        threading.Thread(target=self.simulation.train).start()
        while not self.all_data :
            print("waiting for first game to finish")
            time.sleep(1)
        self.display = Display(self)
        


if __name__ == "__main__":
    App()