import settings
import random
import numpy as np
from plant import Plant

class Prey:

    def __init__(self, game, pos, heritage_stats):
        self.game = game
        self.pos = pos
        self.heritage_stats = heritage_stats
        self.hp = random.randint(settings.PREY_MIN_STARTING_HEALTH_POINTS, settings.PREY_MAX_STARTING_HEALTH_POINTS)
        self.starting_hp = self.hp

        self.test = np.array([0,0,0,0,0,0,0,0])
        
        if game.map_per_tick[pos[0],pos[1]] != 0:
            if game.get_random_free_pos(self.pos):
                self.pos = game.get_random_free_pos(self.pos)
                self.game.map_per_tick[self.pos[0],self.pos[1]] = self
                self.game.prey_list.append(self)
            else:
                del self
        else:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = self
            self.game.prey_list.append(self)

    def regular_action(self): 
        self.eat()       
        self.reproduce_check()
        self.kill_check()
        pass

    def eat(self):
        for direction in [np.array([1,0]),np.array([-1,0]),np.array([0,1]),np.array([0,-1]),np.array([1,1]),np.array([1,-1]),np.array([-1,1]),np.array([-1,-1])]:
            temp = self.pos + direction
            if (temp[0] >= 0 and 
                temp[0] < settings.GRID_WIDTH and 
                temp[1] >= 0 and 
                temp[1] < settings.GRID_HEIGHT and
                isinstance(self.game.map_per_tick[temp[0],temp[1]], Plant)):
                    target = self.game.map_per_tick[temp[0],temp[1]]
                    self.hp += target.hp
                    self.game.reward += self.heritage_stats["eating_reward"]
                    target.hp = 0
                    target.kill_check()
                    self.game.map_per_tick[temp[0],temp[1]] = 0
                    Plant(self.game,
                        np.array([random.randint(0, settings.GRID_WIDTH-1), random.randint(0, settings.GRID_HEIGHT-1)]),
                        settings.generate_plant_heritage_stats()
                        )              
                    break

    def reproduce_check(self):
        # if self.hp >= self.heritage_stats["reproduction_threshold"]:
        #     Prey(self.game, self.pos, self.heritage_stats)
        
        pass
    
    def kill_check(self):
        if self.hp <= 0:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
            self.game.prey_list.remove(self)
            self.game.prey_count -= 1
            del self
        
    def ai_action(self, action):
        
        if action[0] == 1:
            self.move_north()
        elif action[1] == 1:
            self.move_south()
        elif action[2] == 1:
            self.move_east()
        elif action[3] == 1:
            self.move_west()
        elif action[4] == 1:
            self.move_northeast()
        elif action[5] == 1:
            self.move_northwest()
        elif action[6] == 1:
            self.move_southeast()
        elif action[7] == 1:
            self.move_southwest()
            
    def move_north(self):
        if self.pos[1] > 0:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
            self.pos += np.array([0, -1])
            self.game.map_per_tick[self.pos[0],self.pos[1]] = self
        else:
            self.hp = 0
    
    def move_south(self):
        if self.pos[1] < settings.GRID_HEIGHT-1:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
            self.pos += np.array([0, 1])
            self.game.map_per_tick[self.pos[0],self.pos[1]] = self
        else:
            self.hp = 0
    
    def move_east(self):
        if self.pos[0] < settings.GRID_WIDTH-1:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
            self.pos += np.array([1, 0])
            self.game.map_per_tick[self.pos[0],self.pos[1]] = self
        else:
            self.hp = 0
    
    def move_west(self):
        if self.pos[0] > 0:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
            self.pos += np.array([-1, 0])
            self.game.map_per_tick[self.pos[0],self.pos[1]] = self
        else:
            self.hp = 0

    def move_northeast(self):
        if self.pos[1] > 0 and self.pos[0] < settings.GRID_WIDTH-1:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
            self.pos += np.array([1, -1])
            self.game.map_per_tick[self.pos[0],self.pos[1]] = self
        else:
            self.hp = 0

    def move_northwest(self):
        if self.pos[1] > 0 and self.pos[0] > 0:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
            self.pos += np.array([-1, -1])
            self.game.map_per_tick[self.pos[0],self.pos[1]] = self        
        else:
            self.hp = 0
    
    def move_southeast(self):
        if self.pos[1] < settings.GRID_HEIGHT-1 and self.pos[0] < settings.GRID_WIDTH-1:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
            self.pos += np.array([1, 1])
            self.game.map_per_tick[self.pos[0],self.pos[1]] = self
        else:
            self.hp = 0

    def move_southwest(self):
        if self.pos[1] < settings.GRID_HEIGHT-1 and self.pos[0] > 0:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
            self.pos += np.array([-1, 1])
            self.game.map_per_tick[self.pos[0],self.pos[1]] = self
        else:
            self.hp = 0

                
if __name__ == "__main__":
    exec(open("simulation.py").read())
