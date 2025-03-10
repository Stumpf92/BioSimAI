import random
import settings
import numpy as np
# from plant import Plant
# from prey import Prey
# from hunter import Hunter
from creature import Plant, Prey, Hunter
from agent import Agent


class Game:

    def __init__(self, simulation):

        self.simulation = simulation
        self.terrain = simulation.terrain.terrain_map


        self.n_tick_counter = -1
        self.plant_count = 0
        self.prey_count = 0
        self.reward = 0
        self.cum_reward = 0

        self.map_per_tick = np.zeros([settings.GRID_WIDTH,
                                      settings.GRID_HEIGHT], dtype=object)

        self.game_over = False


    def reset(self):

        # set everthing to start
        self.n_tick_counter = -1
        self.plant_count = 0
        self.prey_count = 0
        self.reward = 0
        self.cum_reward = 0

        self.map_per_tick = np.zeros([settings.GRID_WIDTH,
                                      settings.GRID_HEIGHT], dtype=object)
        self.game_over = False

        # spawn creatures
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
                settings.generate_prey_heritage_stats()
                ) 

        self.n_tick_counter += 1

    def play_step(self):

        self.reward = 0
        
        list_of_plants = []
        list_of_preys = []
        list_of_hunters = []

        for x in range(settings.GRID_WIDTH):
            for y in range(settings.GRID_HEIGHT):
                if isinstance(self.map_per_tick[x,y], Plant):
                    list_of_plants.append(self.map_per_tick[x,y])
                elif isinstance(self.map_per_tick[x,y], Prey):
                    list_of_preys.append(self.map_per_tick[x,y])
                elif isinstance(self.map_per_tick[x,y], Hunter):
                    list_of_hunters.append(self.map_per_tick[x,y])

        for _ in list_of_plants:
            _.action()
        for _ in list_of_preys:
            self.reward += _.action()
        for _ in list_of_hunters:
            self.reward += _.action()

        self.plant_count = len(list_of_plants)
        self.prey_count = len(list_of_preys)
        self.hunter_count = len(list_of_hunters)

        # Endcondition
        if (self.n_tick_counter == settings.MAX_TICKS_PER_GAME-2 or
             self.prey_count == 0 or
               self.plant_count == 0 or
                 self.hunter_count == 0):
            self.game_over = True

        # add the reward for one tick to the cummulative score for the whole game
        self.cum_reward += self.reward

        self.n_tick_counter += 1
        # return 
        return self.n_tick_counter, self.map_per_tick, self.plant_count, self.prey_count, self.hunter_count, self.reward, self.cum_reward, self.game_over
    
    def get_random_free_pos(self, position):
        directions = [np.array([0, 1]), np.array([0, -1]), np.array([1, 0]), np.array([-1, 0]), np.array([1, 1]), np.array([-1, -1]), np.array([1, -1]), np.array([-1, 1])]
        random.shuffle(directions)
        while len(directions) > 0:
            direction = directions.pop()
            new_pos = (position[0] + direction[0], position[1] + direction[1])
            if (new_pos[0] >= 0 and 
                new_pos[0] < settings.GRID_WIDTH and 
                new_pos[1] >= 0 and 
                new_pos[1] < settings.GRID_HEIGHT and
                self.map_per_tick[new_pos[0],new_pos[1]] == 0):
                return new_pos
        
        return None



if __name__ == "__main__":
    exec(open("main.py").read())
