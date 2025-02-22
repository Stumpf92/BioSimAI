import pygame as pg
import random
import settings
import numpy as np
from plant import Plant
from prey import Prey
from agent import Agent


class Game:

    def __init__(self, simulation):

        self.simulation = simulation
        self.terrain = simulation.terrain.terrain_map


        self.frame_iteration = 0
        self.plant_count = 0
        self.prey_count = 0
        self.reward = 0
        self.score = 0

        self.map_per_tick = np.zeros([settings.GRID_WIDTH,
                                      settings.GRID_HEIGHT], dtype=object)

        self.game_over = False


    def reset(self):

        # set everthing to start
        self.frame_iteration = 0
        self.plant_count = 0
        self.prey_count = 0
        self.reward = 0
        self.score = 0

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


    def play_step(self):

        self.reward = 0
        self.plant_count = 0
        self.prey_count = 0
    
        

        for x in range(settings.GRID_WIDTH):
            for y in range(settings.GRID_HEIGHT):
                if isinstance(self.map_per_tick[x,y], Plant):
                    self.map_per_tick[x,y].action()
                if isinstance(self.map_per_tick[x,y], Prey):
                    self.reward += self.map_per_tick[x,y].action()
        
        for x in range(settings.GRID_WIDTH):
            for y in range(settings.GRID_HEIGHT):
                if isinstance(self.map_per_tick[x,y], Plant):
                    self.plant_count += 1
                if isinstance(self.map_per_tick[x,y], Prey):
                    self.prey_count += 1
        

        # Endcondition
        if (self.frame_iteration >= settings.MAX_TICKS_PER_GAME or
             self.prey_count == 0 or
               self.plant_count == 0):
            if self.prey_count == 0:
                self.reward -= 1000
            self.game_over = True

        # add the reward for one tick to the cummulative score for the whole game
        self.score += self.reward

        self.frame_iteration += 1
        # return 
        return self.frame_iteration, self.reward, self.game_over, self.score, self.map_per_tick, self.plant_count, self.prey_count
    
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
    exec(open("simulation.py").read())
