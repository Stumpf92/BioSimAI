import settings
import random
random.seed(settings.SEED)
import numpy as np
np.random.seed(settings.SEED)
from creature import Plant, Prey, Hunter, Seed

class Game:

    def __init__(self, simulation):

        self.simulation = simulation
        self.terrain = simulation.terrain.terrain_map



    def reset(self):
        # setzt das Spiel wieder auf Start zurück

        self.n_tick_counter = -1
        self.plant_count = 0
        self.prey_count = 0
        self.hunter_count = 0
        self.seed_count = 0
        self.prey_reward = 0
        self.prey_cum_reward = 0
        self.hunter_reward = 0
        self.hunter_cum_reward = 0

        self.plantmap_per_tick = np.zeros([settings.GRID_WIDTH,
                                      settings.GRID_HEIGHT], dtype=int)
        self.preymap_per_tick = np.zeros([settings.GRID_WIDTH,
                                      settings.GRID_HEIGHT], dtype=int)
        self.huntermap_per_tick = np.zeros([settings.GRID_WIDTH,
                                      settings.GRID_HEIGHT], dtype=int)
        self.seedmap_per_tick = np.zeros([settings.GRID_WIDTH,
                                      settings.GRID_HEIGHT], dtype=int)
        
        self.list_of_plants = []
        self.list_of_preys = []
        self.list_of_hunters = []
        self.list_of_seeds = [] 
        
        
        
        self.game_over = False

        # # spawn creatures
        for _ in range(settings.PLANT_COUNT_START):
            Plant(self.simulation,
                np.array([random.randint(0, settings.GRID_WIDTH-1), random.randint(0, settings.GRID_HEIGHT-1)]),
                settings.generate_plant_heritage_stats()
                )
                
        for _ in range(settings.PREY_COUNT_START):
            Prey(self.simulation,
                np.array([random.randint(0, settings.GRID_WIDTH-1), random.randint(0, settings.GRID_HEIGHT-1)]),
                settings.generate_prey_heritage_stats()
                ) 
        for _ in range(settings.HUNTER_COUNT_START):
            Hunter(self.simulation,
                np.array([random.randint(0, settings.GRID_WIDTH-1), random.randint(0, settings.GRID_HEIGHT-1)]),
                settings.generate_hunter_heritage_stats()
                ) 
        for _ in range(settings.SEED_COUNT_START):
            Seed(self.simulation,
                np.array([random.randint(0, settings.GRID_WIDTH-1), random.randint(0, settings.GRID_HEIGHT-1)]),
                settings.generate_plant_heritage_stats()
                ) 

    def play_step(self):
        # spielt ein Schritt /Tick im Spiel für jeden Agenten und gibt Werte zurück
        
        self.n_tick_counter += 1

        self.prey_reward = 0
        self.hunter_reward = 0        
      

        for _ in self.list_of_plants:
            _.action()
        for _ in self.list_of_preys:
            self.prey_reward += _.action()
        for _ in self.list_of_hunters:
            self.hunter_reward += _.action()
        for _ in self.list_of_seeds:
            _.action()

        self.plant_count = len(self.list_of_plants)
        self.prey_count = len(self.list_of_preys)
        self.hunter_count = len(self.list_of_hunters)
        self.seed_count = len(self.list_of_seeds)


        # Endcondition
        if ((self.n_tick_counter == min(settings.MAX_ENDING_TICKS_PER_GAME,int((settings.MAX_STARTING_TICKS_PER_GAME -1)/min(self.simulation.prey_agent.epsilon, self.simulation.hunter_agent.epsilon)))) or
             (self.prey_count == 0 and settings.PREY_COUNT_START > 0) or
               (self.plant_count == 0 and settings.PLANT_COUNT_START > 0)or
                 (self.hunter_count == 0 and settings.HUNTER_COUNT_START > 0) or
                  ((self.seed_count == 0 and self.plant_count == 0) and settings.SEED_COUNT_START > 0)):
            self.game_over = True

        # add the reward for one tick to the cummulative score for the whole game
        self.prey_cum_reward += self.prey_reward
        self.hunter_cum_reward += self.hunter_reward

        # return 
        return (self.n_tick_counter,
                 self.plantmap_per_tick,
                 self.preymap_per_tick,
                 self.huntermap_per_tick,
                 self.seedmap_per_tick,
                   self.plant_count,
                     self.prey_count,
                       self.hunter_count,
                        self.seed_count,
                         self.prey_reward,
                           self.prey_cum_reward,
                             self.hunter_reward,
                               self.hunter_cum_reward,
                                 self.game_over)
    
    def get_random_free_pos(self, position):
        # wenn position belget , gibt diese Funktion eine zufällige benachbarte freie Position zurück oder eben None wenn keine Position frei sind.
        directions = [np.array([0, 1]), np.array([0, -1]), np.array([1, 0]), np.array([-1, 0]), np.array([1, 1]), np.array([-1, -1]), np.array([1, -1]), np.array([-1, 1])]
        random.shuffle(directions)
        while len(directions) > 0:
            direction = directions.pop()
            new_pos = (position[0] + direction[0], position[1] + direction[1])
            if (new_pos[0] >= 0 and 
                new_pos[0] < settings.GRID_WIDTH and 
                new_pos[1] >= 0 and 
                new_pos[1] < settings.GRID_HEIGHT and
                (self.plantmap_per_tick[new_pos[0],new_pos[1]] == 0 and
                self.preymap_per_tick[new_pos[0],new_pos[1]] == 0 and
                self.huntermap_per_tick[new_pos[0],new_pos[1]] == 0 and
                self.seedmap_per_tick[new_pos[0],new_pos[1]] == 0)):
                return new_pos
        
        return None



if __name__ == "__main__":
    exec(open("main.py").read())
