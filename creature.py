import settings
import random
import numpy as np

class Creature:

    def __init__(self, simulation, pos, heritage_stats):
        self.simulation = simulation
        self.game = simulation.game
        self.pos = pos
        self.heritage_stats = heritage_stats
        self.hp = random.randint(self.heritage_stats["min_starting_hp"], self.heritage_stats["max_starting_hp"])
        self.starting_hp = self.hp
        
        if self.game.map_per_tick[self.pos[0],self.pos[1]] != 0:
            if self.game.get_random_free_pos(self.pos):
                self.pos = self.game.get_random_free_pos(self.pos)
                self.game.map_per_tick[self.pos[0],self.pos[1]] = self
            else:
                del self
        else:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = self
    
    def reproduce_check(self):
        if self.hp >= self.heritage_stats["reproduction_threshold"]:
            self.hp = random.randint(self.heritage_stats["min_starting_hp"], self.heritage_stats["max_starting_hp"])
            if isinstance(self, Plant):
                Plant(self.simulation, self.pos, self.heritage_stats)
            elif isinstance(self, Prey):
                Prey(self.simulation, self.pos, self.heritage_stats)
            elif isinstance(self, Hunter):
                Hunter(self.simulation, self.pos, self.heritage_stats)
        pass

    def kill_check(self):
        if self.hp <= 0:
            self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
            del self

    
    def move_and_or_eat(self, move, food):
        reward = 0
        if move[0] == 1: #north
            vector = np.array([0, -1])            
        elif move[1] == 1: # south
            vector = np.array([0, 1])
        elif move[2] == 1: # east
            vector = np.array([1, 0])
        elif move[3] == 1:# west
            vector = np.array([-1, 0])
        elif move[4] == 1:# northeast
            vector = np.array([1, -1])
        elif move[5] == 1:# northwest
            vector = np.array([-1, -1])
        elif move[6] == 1:# southeast
            vector = np.array([1, 1])
        elif move[7] == 1:# southwest
            vector = np.array([-1, 1])

        new_pos = self.pos + vector

        if (new_pos[0] >= 0 and
            new_pos[0] < settings.GRID_WIDTH and
            new_pos[1] >= 0 and
            new_pos[1] < settings.GRID_HEIGHT):
            if isinstance(self.simulation.game.map_per_tick[new_pos[0], new_pos[1]], food):
                # Prey fressen
                target = self.game.map_per_tick[new_pos[0],new_pos[1]]
                self.hp = min(self.hp+target.hp, self.heritage_stats["max_hp"])
                target.hp = 0
                target.kill_check()
                # und dann auf das Preyfeld ziehen
                self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
                self.pos = new_pos
                self.game.map_per_tick[self.pos[0],self.pos[1]] = self
                #belohnen fürs essen
                reward += self.heritage_stats["eating_bonus"]
            elif self.simulation.game.map_per_tick[new_pos[0], new_pos[1]] != 0 and isinstance(self.simulation.game.map_per_tick[new_pos[0], new_pos[1]], food) == False:
                # Punish für dämlichen Movement-Versuch
                reward += self.heritage_stats["stupid_malus"]

            elif self.simulation.game.map_per_tick[new_pos[0], new_pos[1]] == 0:
                # eigentliche Bewegung
                self.game.map_per_tick[self.pos[0],self.pos[1]] = 0
                self.pos = new_pos
                self.game.map_per_tick[self.pos[0],self.pos[1]] = self
            
            
        else:
            reward += self.heritage_stats["stupid_malus"]
        
        return reward
    
    def detect_nearest_target(self, target_type, distance_range = max(settings.GRID_WIDTH, settings.GRID_HEIGHT)):
        pos = self.pos
        for i in range(1,distance_range+1):
            vectors = []
            for x in range(-i,i+1):
                for y in range(-i,i+1):
                    vectors.append(np.array([x,y]))
            random.shuffle(vectors)
            while len(vectors) > 0:
                vector = vectors.pop()
                new_pos = (pos[0] + vector[0], pos[1] + vector[1])
                if (new_pos[0] >= 0 and
                     new_pos[0] < settings.GRID_WIDTH and
                       new_pos[1] >= 0 and
                         new_pos[1] < settings.GRID_HEIGHT and
                            isinstance(self.game.map_per_tick[pos[0]+vector[0],pos[1]+vector[1]], target_type)):
                    return self.game.map_per_tick[new_pos]
                    break
        return 0



class Plant(Creature):

    def __init__(self, simulation, pos, heritage_stats):
        super().__init__(simulation, pos, heritage_stats)

    def action(self):
        self.kill_check()
        self.grow()
        self.reproduce_check()
    
    def grow(self):
        self.hp = min(self.hp +self.heritage_stats["growth_rate"], self.heritage_stats["max_hp"])




class Prey(Creature):

    def __init__(self, simulation, pos, heritage_stats):
        super().__init__(simulation, pos, heritage_stats)
    
    def action(self): 
        game_over = False ### ACHTUNG, das muss noch überprüft werden

        reward = 0
        ##identify closest target
        target = self.detect_nearest_target(Plant)
        # get old state
        state_old = self.simulation.prey_agent.get_state(self, target)
        if target !=0:
            distance_before = max(abs(self.pos[0]-target.pos[0]), abs(self.pos[1]-target.pos[1]))
        # get move
        final_move = self.simulation.prey_agent.get_action(state_old)
        #make the move       
        reward += self.move_and_or_eat(final_move, Plant)
        if target !=0:
            distance_after = max(abs(self.pos[0]-target.pos[0]), abs(self.pos[1]-target.pos[1]))
        #rewarding for moving closer
        if target !=0:
            if distance_before > distance_after:
                reward += self.heritage_stats["getting_closer_bonus"]
        #punish for moving away
        else:
            reward += -10
        # get new state
        state_new = self.simulation.prey_agent.get_state(self, target)
        #train
        self.simulation.prey_agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        # remember
        self.simulation.prey_agent.remember(state_old, final_move, reward, state_new, game_over)

        ###extra stuff
        self.kill_check()
     
        self.reproduce_check()

        return reward

class Hunter(Creature):

    def __init__(self, simulation, pos, heritage_stats):
        super().__init__(simulation, pos, heritage_stats)


    def action(self): 
        game_over = False ### ACHTUNG, das muss noch überprüft werden

        reward = 0
        ##identify closest target
        target = self.detect_nearest_target(Prey)
        # get old state
        state_old = self.simulation.hunter_agent.get_state(self, target)
        if target !=0:
            distance_before = max(abs(self.pos[0]-target.pos[0]), abs(self.pos[1]-target.pos[1]))
        # get move
        final_move = self.simulation.hunter_agent.get_action(state_old)
        #make the move       
        reward += self.move_and_or_eat(final_move, Prey)
        if target !=0:
            distance_after = max(abs(self.pos[0]-target.pos[0]), abs(self.pos[1]-target.pos[1]))
        #rewarding for moving closer
        if target !=0:
            if distance_before > distance_after:
                reward += self.heritage_stats["getting_closer_bonus"]
        #punish for moving away
        else:
            reward += -10
        # get new state
        state_new = self.simulation.hunter_agent.get_state(self, target)
        #train
        self.simulation.hunter_agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        # remember
        self.simulation.hunter_agent.remember(state_old, final_move, reward, state_new, game_over)

        ###extra stuff
        self.kill_check()
     
        self.reproduce_check()

        return reward
            
    
            

if __name__ == "__main__":
    exec(open("main.py").read())
