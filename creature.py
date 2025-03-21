import settings
import random
random.seed(settings.SEED)
import numpy as np
np.random.seed(settings.SEED)
import math

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
        # kontrolliert und löst Vermehrung aus
        if random.random() > math.sqrt(min(self.simulation.prey_agent.epsilon, self.simulation.hunter_agent.epsilon)):
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
        # kontrolliert und löst Kill aus
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
        # reduziert die Creaturen bei überschreiten der maximalen Anzahl "max_global_count"
        if isinstance(self,Plant):
            amount = len(self.game.list_of_plants)
        elif isinstance(self,Prey):
            amount = len(self.game.list_of_preys)
        elif isinstance(self,Hunter):
            amount = len(self.game.list_of_hunters)
        elif isinstance(self,Seed):
            amount = len(self.game.list_of_seeds)
        
        if amount > self.heritage_stats["max_global_count"]:
            self.hp -= (((amount - self.heritage_stats["max_global_count"])/self.heritage_stats["max_global_count"])*(self.heritage_stats["max_hp"]))**(1/8)

        # self.hp -= self.heritage_stats["max_hp"]
        # self.hp -= self.heritage_stats["decay_rate"]*self.heritage_stats["max_hp"]

        self.kill_check()
    
    def move_and_or_eat(self, move, food): 
        # führt Bewegung und ggf das Essen aus
        reward = 0
        if move[0] == 1: 
            vector = np.array([0, -1])            
        elif move[1] == 1: 
            vector = np.array([0, 1])
        elif move[2] == 1: 
            vector = np.array([1, 0])
        elif move[3] == 1:
            vector = np.array([-1, 0])
        elif move[4] == 1:
            vector = np.array([1, -1])
        elif move[5] == 1:
            vector = np.array([-1, -1])
        elif move[6] == 1:
            vector = np.array([1, 1])
        elif move[7] == 1:
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
                    if random.random() > math.sqrt(min(self.simulation.prey_agent.epsilon, self.simulation.hunter_agent.epsilon)):
                        if random.random() < food_target.heritage_stats["seed_chance"]:
                            self.seed_heritage_stats = food_target.heritage_stats
                            self.seed_state = True
                            self.seed_transport_timer = 0
                    if random.random() < math.sqrt(min(self.simulation.prey_agent.epsilon, self.simulation.hunter_agent.epsilon)):
                        Plant(self.simulation,
                            np.array([random.randint(0, settings.GRID_WIDTH-1), random.randint(0, settings.GRID_HEIGHT-1)]),
                            settings.generate_plant_heritage_stats())
                        
                if isinstance(food_target, Prey):
                    if random.random() < math.sqrt(min(self.simulation.prey_agent.epsilon, self.simulation.hunter_agent.epsilon)):
                        Prey(self.simulation,
                            np.array([random.randint(0, settings.GRID_WIDTH-1), random.randint(0, settings.GRID_HEIGHT-1)]),
                            settings.generate_prey_heritage_stats())
                        
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
                reward += self.heritage_stats["eating_reward_bonus"]

            elif (self.game.plantmap_per_tick[new_pos[0], new_pos[1]] != 0 or 
                  self.game.preymap_per_tick[new_pos[0], new_pos[1]] != 0 or 
                  self.game.huntermap_per_tick[new_pos[0], new_pos[1]] != 0):
                # Punish für dämlichen Movement-Versuch
                reward += self.heritage_stats["friend_collision_reward_malus"]

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
            reward += self.heritage_stats["wall_collision_reward_malus"]
        
        return reward
    
    def seed_check(self):
        # wenn einer Creature ein Seed anhängt wird hier gecheckt ob der eigentliche Seed spawnen soll
        self.seed_transport_timer += 1
        if self.seed_transport_timer == self.seed_heritage_stats["seed_transport_max_timer"]:
            Seed(self.simulation, self.pos, self.seed_heritage_stats)
            self.seed_state = False
            self.seed_transport_timer = 0
    
    def calc_danger_matrix(self, vision_radius, reward_radius):
        # vision_matrix = Zeigt die Creatures in der Umgebung(vision_radius) einer Creature in einer Matrix an. 
        # reward_matrix = zeigt eine Matrix in der Umgebung(reward_radius) um eine Creature mit den Werten der möglichen Belohnungen und Bestrafungen
        # reward_matrix_sum = Summe der Werte aus reward_ Matrix. Maß dafür ob agent sich in freundlciher oder feindlicher Umgebung befindet
        vision_matrix = np.zeros((vision_radius*2+1,vision_radius*2+1))
        reward_matrix = np.zeros((reward_radius*2+1,reward_radius*2+1))

        origin_vision_matrix = (self.pos[0]-vision_radius, self.pos[1]-vision_radius)        
        for y_vision_matrix in range(vision_matrix.shape[1]):
            for x_vision_matrix in range(vision_matrix.shape[0]):
                if (origin_vision_matrix[0]+x_vision_matrix >= 0 and
                    origin_vision_matrix[0]+x_vision_matrix < settings.GRID_WIDTH and
                    origin_vision_matrix[1]+y_vision_matrix >= 0 and
                    origin_vision_matrix[1]+y_vision_matrix < settings.GRID_HEIGHT):
                    if self.game.plantmap_per_tick[origin_vision_matrix[0]+x_vision_matrix,origin_vision_matrix[1]+y_vision_matrix] == 1:
                        if self.food == Plant:
                            vision_matrix[x_vision_matrix,y_vision_matrix] = self.heritage_stats["eating_reward_bonus"]
                        elif self.enemy == Plant:
                            vision_matrix[x_vision_matrix,y_vision_matrix] = self.heritage_stats["enemy_collision_reward_malus"] 
                        elif self.friend == Plant:
                            vision_matrix[x_vision_matrix,y_vision_matrix] = self.heritage_stats["friend_collision_reward_malus"]
                    elif self.game.preymap_per_tick[origin_vision_matrix[0]+x_vision_matrix,origin_vision_matrix[1]+y_vision_matrix] == 1:
                        if self.food == Prey:
                            vision_matrix[x_vision_matrix,y_vision_matrix] = self.heritage_stats["eating_reward_bonus"]
                        elif self.enemy == Prey:
                            vision_matrix[x_vision_matrix,y_vision_matrix] = self.heritage_stats["enemy_collision_reward_malus"]  *-1
                        elif self.friend == Prey:
                            vision_matrix[x_vision_matrix,y_vision_matrix] = self.heritage_stats["friend_collision_reward_malus"]
                    elif self.game.huntermap_per_tick[origin_vision_matrix[0]+x_vision_matrix,origin_vision_matrix[1]+y_vision_matrix] == 1:
                        if self.food == Hunter:
                            vision_matrix[x_vision_matrix,y_vision_matrix] = self.heritage_stats["eating_reward_bonus"]
                        elif self.enemy == Hunter:
                            vision_matrix[x_vision_matrix,y_vision_matrix] = self.heritage_stats["enemy_collision_reward_malus"]  *-1
                        elif self.friend == Hunter:
                            vision_matrix[x_vision_matrix,y_vision_matrix] = self.heritage_stats["friend_collision_reward_malus"]
                else:                    
                    vision_matrix[x_vision_matrix,y_vision_matrix] = self.heritage_stats["wall_collision_reward_malus"]


        multiplier_matrix = np.ones((2*reward_radius+1, 2*reward_radius+1))
        center_coord = (2*reward_radius+1)//2
        distance = 0

        while center_coord - distance > 0:
            distance += 1
            multiplier_matrix[center_coord-distance,:] = 1/(distance+1)
            multiplier_matrix[center_coord+distance,:] = 1/(distance+1)
            multiplier_matrix[:,center_coord - distance] = 1/(distance+1)
            multiplier_matrix[:,center_coord + distance] = 1/(distance+1)
        
        reward_matrix = vision_matrix[center_coord-reward_radius+1:center_coord+reward_radius+2,center_coord-reward_radius+1:center_coord+reward_radius+2] * multiplier_matrix
            
        reward_matrix_sum = reward_matrix.sum()
        return vision_matrix, reward_matrix, reward_matrix_sum

class Plant(Creature):

    def __init__(self, simulation, pos, heritage_stats):
        super().__init__(simulation, pos, heritage_stats)
        self.friend = Hunter
        self.enemy = Prey
        self.food = None

    def action(self):
        # diese Aktionen führt dieser Agent jeden Tick aus
        self.grow()
        self.decay()
    
    def grow(self):
        # Wachsen, jeden Tick
        self.hp = min(self.hp +self.heritage_stats["growth_rate"], self.heritage_stats["max_hp"])
        self.reproduce_check()




class Prey(Creature):

    def __init__(self, simulation, pos, heritage_stats):
        super().__init__(simulation, pos, heritage_stats)
        self.friend = Prey
        self.enemy = Hunter
        self.food = Plant
    
    def action(self): 
        # diese Aktionen führt dieser Agent jeden Tick aus
        game_over = False ### ACHTUNG, das muss noch überprüft werden
        reward = 0
        danger_matrix_old, reward_matrix_old, reward_matrix_sum_old = self.calc_danger_matrix(self.heritage_stats["vision_radius"], self.heritage_stats["reward_radius"])        
        
        # get old state
        state_old = self.simulation.prey_agent.get_state(danger_matrix_old)
        # get move
        final_move = self.simulation.prey_agent.get_action(state_old)
        #make the move       
        reward += self.move_and_or_eat(final_move, self.food)

        danger_matrix_new, reward_matrix_new, reward_matrix_sum_new = self.calc_danger_matrix(self.heritage_stats["vision_radius"], self.heritage_stats["reward_radius"])   

        
        # get new state     
        state_new = self.simulation.prey_agent.get_state(danger_matrix_new)

        #train
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
        # diese Aktionen führt dieser Agent jeden Tick aus
        game_over = False ### ACHTUNG, das muss noch überprüft werden
        reward = 0

        danger_matrix_old, reward_matrix_old, reward_matrix_sum_old = self.calc_danger_matrix(self.heritage_stats["vision_radius"], self.heritage_stats["reward_radius"])        
        
        # get old state
        state_old = self.simulation.hunter_agent.get_state(danger_matrix_old)
        # get move
        final_move = self.simulation.hunter_agent.get_action(state_old)
        #make the move       
        reward += self.move_and_or_eat(final_move, self.food)

        danger_matrix_new, reward_matrix_new, reward_matrix_sum_new = self.calc_danger_matrix(self.heritage_stats["vision_radius"], self.heritage_stats["reward_radius"])   

        
        # get new state     
        state_new = self.simulation.hunter_agent.get_state(danger_matrix_new)

        #train
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
        # diese Aktionen führt dieser Agent jeden Tick aus
        self.seed_check()
    

    def seed_check(self):
        # checkt ob ein Seed spawnen soll
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
