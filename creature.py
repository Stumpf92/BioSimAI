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
        self.seed_state = False
        self.seed_transport_timer = 0
        self.seed_heritage_stats = None
        
        if (self.game.plantmap_per_tick[self.pos[0],self.pos[1]] == 1 or
            self.game.preymap_per_tick[self.pos[0],self.pos[1]] == 1 or
            self.game.huntermap_per_tick[self.pos[0],self.pos[1]] == 1 or
            self.game.seedmap_per_tick[self.pos[0],self.pos[1]] == 1):
            if self.game.get_random_free_pos(self.pos):
                self.pos = self.game.get_random_free_pos(self.pos)
                if isinstance(self,Plant):
                    self.game.plantmap_per_tick[self.pos[0],self.pos[1]] = 1
                    self.game.list_of_plants.append(self)
                elif isinstance(self,Prey):
                    self.game.preymap_per_tick[self.pos[0],self.pos[1]] = 1
                    self.game.list_of_preys.append(self)
                elif isinstance(self,Hunter):
                    self.game.huntermap_per_tick[self.pos[0],self.pos[1]] = 1
                    self.game.list_of_hunters.append(self)
            else:
                del self
        else:
            if isinstance(self,Plant):
                self.game.plantmap_per_tick[self.pos[0],self.pos[1]] = 1
                self.game.list_of_plants.append(self)
            elif isinstance(self,Prey):
                self.game.preymap_per_tick[self.pos[0],self.pos[1]] = 1
                self.game.list_of_preys.append(self)
            elif isinstance(self,Hunter):
                self.game.huntermap_per_tick[self.pos[0],self.pos[1]] = 1
                self.game.list_of_hunters.append(self)
    
    def reproduce_check(self):
        if self.hp >= self.heritage_stats["reproduction_threshold"]:
            self.hp = random.randint(self.heritage_stats["min_starting_hp"], self.heritage_stats["max_starting_hp"])
            if isinstance(self, Plant):
                Plant(self.simulation, self.pos, self.heritage_stats)
            elif isinstance(self, Prey):
                Prey(self.simulation, self.pos, self.heritage_stats)
            elif isinstance(self, Hunter):
                Hunter(self.simulation, self.pos, self.heritage_stats)
        

    def kill_check(self):
        if self.hp <= 0:
            if isinstance(self,Plant):
                self.game.plantmap_per_tick[self.pos[0],self.pos[1]] = 0
                self.game.list_of_plants.remove(self)
            elif isinstance(self,Prey):
                self.game.preymap_per_tick[self.pos[0],self.pos[1]] = 0
                self.game.list_of_preys.remove(self)
            elif isinstance(self,Hunter):
                self.game.huntermap_per_tick[self.pos[0],self.pos[1]] = 0
                self.game.list_of_hunters.remove(self)
            elif isinstance(self,Seed):
                self.game.seedmap_per_tick[self.pos[0],self.pos[1]] = 0
                self.game.list_of_seeds.remove(self)
            del self

    def decay(self):
        self.hp -= self.heritage_stats["decay_rate"]*self.heritage_stats["max_hp"]
        self.kill_check()
    
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
            if ((food == Plant and self.game.plantmap_per_tick[new_pos[0], new_pos[1]] == 1) or 
                (food == Prey and self.game.preymap_per_tick[new_pos[0], new_pos[1]] == 1)):

                # target suchen und um target-hp heilen
                if food == Plant :
                    for element in self.game.list_of_plants:
                        if element.pos[0] == new_pos[0] and element.pos[1] == new_pos[1]:
                            food_target = element
                elif food == Prey:
                    for element in self.game.list_of_preys:
                        if element.pos[0] == new_pos[0] and element.pos[1] == new_pos[1]:
                            food_target = element
                # heal
                
                self.hp = min(self.hp + int(self.heritage_stats["eating_heal"]*self.heritage_stats["max_hp"]),
                                self.heritage_stats["max_hp"])

                # eventuell seeden, wenn food = Plant
                if isinstance(food_target, Plant):
                    if random.random() < food_target.heritage_stats["seed_chance"]:
                        self.seed_heritage_stats = food_target.heritage_stats
                        self.seed_state = True
                        self.seed_transport_timer = 0

                # target töten
                food_target.hp = 0
                food_target.kill_check()  
                # und dann selbst auf das Feld ziehen
                if isinstance(self,Plant):
                    self.game.plantmap_per_tick[self.pos[0],self.pos[1]] = 0
                    self.pos = new_pos
                    self.game.plantmap_per_tick[self.pos[0],self.pos[1]] = 1
                elif isinstance(self,Prey):
                    self.game.preymap_per_tick[self.pos[0],self.pos[1]] = 0
                    self.pos = new_pos
                    self.game.preymap_per_tick[self.pos[0],self.pos[1]] = 1
                elif isinstance(self,Hunter):
                    self.game.huntermap_per_tick[self.pos[0],self.pos[1]] = 0
                    self.pos = new_pos
                    self.game.huntermap_per_tick[self.pos[0],self.pos[1]] = 1
               

                            
                self.reproduce_check() 
                reward += self.heritage_stats["eating_bonus"]

            elif (self.game.plantmap_per_tick[new_pos[0], new_pos[1]] != 0 or 
                  self.game.preymap_per_tick[new_pos[0], new_pos[1]] != 0 or 
                  self.game.huntermap_per_tick[new_pos[0], new_pos[1]] != 0):
                # Punish für dämlichen Movement-Versuch
                reward += self.heritage_stats["stupid_malus"]

            elif (self.game.plantmap_per_tick[new_pos[0], new_pos[1]] == 0 or 
                  self.game.preymap_per_tick[new_pos[0], new_pos[1]] == 0 or 
                  self.game.huntermap_per_tick[new_pos[0], new_pos[1]] == 0):
                # eigentliche Bewegung, wenn Raum ist leer
                if isinstance(self,Plant):
                    self.game.plantmap_per_tick[self.pos[0],self.pos[1]] = 0
                    self.pos = new_pos
                    self.game.plantmap_per_tick[self.pos[0],self.pos[1]] = 1
                elif isinstance(self,Prey):
                    self.game.preymap_per_tick[self.pos[0],self.pos[1]] = 0
                    self.pos = new_pos
                    self.game.preymap_per_tick[self.pos[0],self.pos[1]] = 1
                elif isinstance(self,Hunter):
                    self.game.huntermap_per_tick[self.pos[0],self.pos[1]] = 0
                    self.pos = new_pos
                    self.game.huntermap_per_tick[self.pos[0],self.pos[1]] = 1
               
            
            
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
                         new_pos[1] < settings.GRID_HEIGHT ):
                    if target_type == Plant and self.game.plantmap_per_tick[new_pos[0], new_pos[1]] == 1:
                        for element in self.game.list_of_plants:
                            if element.pos[0] == new_pos[0] and element.pos[1] == new_pos[1]:
                                return element
                    elif target_type == Prey and self.game.preymap_per_tick[new_pos[0], new_pos[1]] == 1:
                        for element in self.game.list_of_preys:
                            if element.pos[0] == new_pos[0] and element.pos[1] == new_pos[1]:
                                return element
                    elif target_type == Hunter and self.game.huntermap_per_tick[new_pos[0], new_pos[1]] == 1:
                        for element in self.game.list_of_hunters:
                            if element.pos[0] == new_pos[0] and element.pos[1] == new_pos[1]:
                                return element
                    elif target_type == Seed and self.game.seedmap_per_tick[new_pos[0], new_pos[1]] == 1:
                        for element in self.game.list_of_seeds:
                            if element.pos[0] == new_pos[0] and element.pos[1] == new_pos[1]:
                                return element
        return 0
    
    def seed_check(self):
        self.seed_transport_timer += 1
        if self.seed_transport_timer == self.seed_heritage_stats["seed_transport_max_timer"]:
            Seed(self.simulation, self.pos, self.seed_heritage_stats)
            self.seed_state = False
            self.seed_transport_timer = 0
    
    def calc_danger_matrix(self, vision_radius):
        matrix = np.zeros((vision_radius*2+1,vision_radius*2+1))
        origin_matrix = (self.pos[0]-vision_radius, self.pos[1]-vision_radius)        
        for y_projection in range(matrix.shape[1]):
            for x_projection in range(matrix.shape[1]):
                if (origin_matrix[0]+x_projection >= 0 and
                    origin_matrix[0]+x_projection < settings.GRID_WIDTH and
                    origin_matrix[1]+y_projection >= 0 and
                    origin_matrix[1]+y_projection < settings.GRID_HEIGHT):
                    if self.game.plantmap_per_tick[origin_matrix[0]+x_projection,origin_matrix[1]+y_projection] == 1:
                        if self.food == Plant:
                            matrix[x_projection,y_projection] = self.heritage_stats["eating_bonus"]
                        elif self.enemy == Plant:
                            matrix[x_projection,y_projection] = self.heritage_stats["eating_bonus"] *-1
                        elif self.friend == Plant:
                            matrix[x_projection,y_projection] = self.heritage_stats["stupid_malus"]
                    elif self.game.preymap_per_tick[origin_matrix[0]+x_projection,origin_matrix[1]+y_projection] == 1:
                        if self.food == Prey:
                            matrix[x_projection,y_projection] = self.heritage_stats["eating_bonus"]
                        elif self.enemy == Prey:
                            matrix[x_projection,y_projection] = self.heritage_stats["eating_bonus"] *-1
                        elif self.friend == Prey:
                            matrix[x_projection,y_projection] = self.heritage_stats["stupid_malus"]
                    elif self.game.huntermap_per_tick[origin_matrix[0]+x_projection,origin_matrix[1]+y_projection] == 1:
                        if self.food == Hunter:
                            matrix[x_projection,y_projection] = self.heritage_stats["eating_bonus"]
                        elif self.enemy == Hunter:
                            matrix[x_projection,y_projection] = self.heritage_stats["eating_bonus"] *-1
                        elif self.friend == Hunter:
                            matrix[x_projection,y_projection] = self.heritage_stats["stupid_malus"]
                else:                    
                    matrix[x_projection,y_projection] = self.heritage_stats["stupid_malus"]
        return matrix

class Plant(Creature):

    def __init__(self, simulation, pos, heritage_stats):
        super().__init__(simulation, pos, heritage_stats)
        self.friend = Hunter
        self.enemy = Prey
        self.food = None

    def action(self):
        self.grow()
        self.decay()
    
    def grow(self):
        self.hp = min(self.hp +self.heritage_stats["growth_rate"], self.heritage_stats["max_hp"])
        self.reproduce_check()




class Prey(Creature):

    def __init__(self, simulation, pos, heritage_stats):
        super().__init__(simulation, pos, heritage_stats)
        self.friend = None
        self.enemy = Hunter
        self.food = Plant
    
    def action(self): 
        game_over = False ### ACHTUNG, das muss noch überprüft werden

        reward = 0
        ##identify closest target
        target = self.detect_nearest_target(Plant)
        #danger_matrix = self.calc_danger_matrix(self.heritage_stats["vision_radius"])
        # get old state
        state_old = self.simulation.prey_agent.get_state(self, target)
        if target !=0:
            distance_before = max(abs(self.pos[0]-target.pos[0]), abs(self.pos[1]-target.pos[1]))
        # get move
        final_move = self.simulation.prey_agent.get_action(state_old)
        #make the move       
        reward += self.move_and_or_eat(final_move, self.food)
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
        reward += self.hp
        self.simulation.prey_agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        # remember
        self.simulation.prey_agent.remember(state_old, final_move, reward, state_new, game_over)

        ###extra stuff
        if self.seed_state:
            self.seed_check()
        self.decay()

        return reward

class Hunter(Creature):

    def __init__(self, simulation, pos, heritage_stats):
        super().__init__(simulation, pos, heritage_stats)
        self.friend = Plant
        self.enemy = None
        self.food = Prey

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
        reward += self.move_and_or_eat(final_move, self.food)
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
        reward += self.hp
        self.simulation.hunter_agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        # remember
        self.simulation.hunter_agent.remember(state_old, final_move, reward, state_new, game_over)

        ###extra stuff
        self.decay()

        return reward
    
class Seed():

    def __init__(self, simulation, pos, heritage_stats):
        self.simulation = simulation
        self.game = simulation.game
        self.pos = pos
        self.heritage_stats = heritage_stats

        self.seed_timer = 0

        if (self.game.seedmap_per_tick[self.pos[0],self.pos[1]] ==1):
            if self.game.get_random_free_pos(self.pos):
                self.pos = self.game.get_random_free_pos(self.pos)
                self.game.seedmap_per_tick[self.pos[0],self.pos[1]] = 1
                self.game.list_of_seeds.append(self)
            else:
                del self
        else:
            self.game.seedmap_per_tick[self.pos[0],self.pos[1]] = 1
            self.game.list_of_seeds.append(self)
    

    
    def action(self):
        self.seed_check()
    

    def seed_check(self):
        self.seed_timer += 1
        if (self.seed_timer >= self.heritage_stats["seed_sprout_max_timer"] and 
            self.game.plantmap_per_tick[self.pos[0],self.pos[1]] == 0 and 
            self.game.preymap_per_tick[self.pos[0],self.pos[1]] == 0 and 
            self.game.huntermap_per_tick[self.pos[0],self.pos[1]] == 0 and 
            self.game.seedmap_per_tick[self.pos[0],self.pos[1]] == 1):

            simulation = self.simulation
            pos = self.pos
            heritage_stats = self.heritage_stats
            self.game.list_of_seeds.remove(self)
            self.game.seedmap_per_tick[self.pos[0],self.pos[1]] = 0
            del self
            Plant(simulation, pos, heritage_stats)     
    
            

if __name__ == "__main__":
    exec(open("main.py").read())
