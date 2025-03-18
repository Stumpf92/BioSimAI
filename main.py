import threading
from simulation import Simulation
from display import Display




class App:
    def __init__(self):


        self.simulation_mode = True
        self.display_mode = True   

        # data channel , reaching over both threads
        self.all_data = []

        # starts the virtual world and the learning process
        self.simulation = Simulation(self)
        self.thread = threading.Thread(target=self.simulation.train).start()        

        # starts the UI
        self.display = Display(self)

        


if __name__ == "__main__":
    App()
