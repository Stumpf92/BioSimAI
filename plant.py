# import settings
# import random
# class Plant:

    # def __init__(self, simulation, pos, heritage_stats):
    #     self.simulation = simulation
    #     self.game = simulation.game
    #     self.pos = pos
    #     self.heritage_stats = heritage_stats
    #     self.hp = random.randint(self.heritage_stats["min_starting_hp"], self.heritage_stats["max_starting_hp"])
    #     self.starting_hp = self.hp
        
    #     if self.game.map_per_tick[self.pos[0],self.pos[1]] != 0:
    #         if self.game.get_random_free_pos(self.pos):
    #             self.pos = self.game.get_random_free_pos(self.pos)
    #             self.game.map_per_tick[self.pos[0],self.pos[1]] = self
    #         else:
    #             del self
    #     else:
    #         self.game.map_per_tick[self.pos[0],self.pos[1]] = self


    # def action(self):
    #     self.kill_check()
    #     self.grow()
    #     self.reproduce_check()


    # def grow(self):
    #     self.hp = min(self.hp +self.heritage_stats["growth_rate"], self.heritage_stats["max_hp"])
            

#     def reproduce_check(self):
#         if self.hp >= self.heritage_stats["reproduction_threshold"]:
#             self.hp = random.randint(self.heritage_stats["min_starting_hp"], self.heritage_stats["max_starting_hp"])
#             Plant(self.simulation, self.pos, self.heritage_stats)
#         pass
    
#     def kill_check(self):
#         if self.hp <= 0:
#             self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
#             del self
            

# if __name__ == "__main__":
#     exec(open("main.py").read())
