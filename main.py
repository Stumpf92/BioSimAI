import threading
from simulation import Simulation
from display import Display


class App:
    def __init__(self):
        self.simulation_mode = False
        self.display_mode = False


        self.simulation = Simulation(self)
        self.all_data = []

        self.thread = threading.Thread(target=self.simulation.train).start()
        self.display = Display(self)

        


if __name__ == "__main__":
    App()