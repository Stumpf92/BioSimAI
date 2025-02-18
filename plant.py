import settings
import random
class Plant:

    def __init__(self, game, pos, heritage_stats):
        self.game = game
        self.pos = pos
        self.heritage_stats = heritage_stats
        self.hp = random.randint(settings.PLANT_MIN_STARTING_HEALTH_POINTS, settings.PLANT_MAX_STARTING_HEALTH_POINTS)
        self.starting_hp = self.hp
        
        if game.map_per_tick[self.pos[0],self.pos[1]] != 0:
            if game.get_random_free_pos(self.pos):
                self.pos = game.get_random_free_pos(self.pos)
                self.game.map_per_tick[self.pos[0],self.pos[1]] = self
                self.game.plant_list.append(self)
            else:
                del self
        else:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = self
            self.game.plant_list.append(self)


    def regular_action(self):
        self.grow()
        self.reproduce_check()
        self.kill_check()

    def grow(self):
        self.hp += self.heritage_stats["growth_rate"]
        if self.hp > self.heritage_stats["max_hp_multiplier"]*self.heritage_stats["reproduction_threshold"]: 
            self.hp = self.heritage_stats["max_hp_multiplier"]*self.heritage_stats["reproduction_threshold"]
            

    def reproduce_check(self):
        # if self.hp >= self.heritage_stats["reproduction_threshold"]:
        #     self.hp = random.randint(settings.PLANT_MIN_STARTING_HEALTH_POINTS, settings.PLANT_MAX_STARTING_HEALTH_POINTS)
        #     Plant(self.game, self.pos, self.heritage_stats)
        pass
    
    def kill_check(self):
        if self.hp <= 0:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
            self.game.plant_list.remove(self)
            self.game.plant_count -= 1
            del self
            

if __name__ == "__main__":
    exec(open("simulation.py").read())
