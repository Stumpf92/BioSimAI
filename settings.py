import random
import torch

#OVERALL
#SEED = 3
SEED = random.randint(0, 1000)
random.seed(SEED)

#DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DEVICE = torch.device("cpu")

####SIMULATION SETTINGS
MAX_GAMES_PER_SIMULATION = 1000

###GAME SETTINGS

MAX_STARTING_TICKS_PER_GAME = 100  # 1000
MAX_ENDING_TICKS_PER_GAME = 1000
PLANT_COUNT_START = 30  #30
PREY_COUNT_START = 15   # 15
HUNTER_COUNT_START = 0  #10
SEED_COUNT_START = 0  #3

GRID_WIDTH = 35       #35
GRID_HEIGHT = 35     #35



####DISPLAY SETTINGS

DISPLAY_MODE = True
DISPLAY_REDUCTION_FACTOR = 20
TITLE = "BioSim"
X_OFFSET = 20
Y_OFFSET = 20

GRID_SIZE = 12

DIAGRAM_WIDTH = 5
DIAGRAM_HEIGHT = 3

BACKGROUND_COLOR = (100 , 100, 100)
FPS= 30



### Plot settings

PLOT_MODE = True
PLOT_REDUCTION_FACTOR = 1

#Terrain_settings:
TERRAIN_ACTIVATION_MODE = True 
TERRAIN_SEED =  random.randint(0, 1000)   
TERRAIN_NOISE_ZOOM = 20 
TERRAIN_MAX_HEIGHT = 10    #From 1 to Terrain_MAX_HEIGHT
TERRAIN_BASE_COLOR = (100, 100, 100)
TERRAIN_COLOR_STEP = 7

RIVER_ACTIVATION_MODE = False
WATER_COLOR = (0,0,255)


#Plant stats
def generate_plant_heritage_stats():
    return {
        "generation": 0,
        "min_starting_hp":5,
        "max_starting_hp":50,
        "max_hp":100,
        "max_global_count": 100,
        "reproduction_threshold": 80,
        "growth_rate": random.randint(80, 105)/100,
        "max_hp_multiplier": 1.1,
        "ticks_per_action": 8,
        "ticks_per_mutation": 0,
        "decay_rate": 0.001,
        "seed_transport_max_timer": random.randint(6, 30),
        "seed_sprout_max_timer": random.randint(40, 150),
        "seed_chance": random.randint(5, 15)/100,}


#Prey stats
def generate_prey_heritage_stats():     
    return {
        "generation": 0,
        "min_starting_hp":30,
        "max_starting_hp":120,
        "max_hp":250,        
        "max_global_count": 50,
        "reproduction_threshold": 230,
        "decay_rate": 0.002,
        "wall_collision_reward_malus": -2, #-2
        "friend_collision_reward_malus": -1, #-0.1
        "enemy_collision_reward_malus": -5,
        "eating_reward_bonus": 5,
        "eating_heal": random.randint(30, 55)/100,
        "terrain_malus_multiplier": 0,
        "vision_radius": 5,
        "reward_radius": 1,
        "max_memory" :100000,
        "batch_size" :1000,
        "lr" :0.001,
        "gamma" :0.9,
        "epsilon_decay" :0.999997,
        "min_epsilon" :0.01,
        }

#Hunter stats
def generate_hunter_heritage_stats():
    return {
        "generation": 0,
        "min_starting_hp":80,
        "max_starting_hp":450,
        "max_hp":700,
        "max_global_count": 15,
        "reproduction_threshold": 600,
        "decay_rate": 0.007,
        "seeding_probability": 0.05,
        "wall_collision_reward_malus": -2, #-2
        "friend_collision_reward_malus": -1, #-0.1
        "enemy_collision_reward_malus": -5,
        "eating_reward_bonus": 5,
        "eating_heal": random.randint(30, 55)/100,
        "getting_closer_bonus": 20,
        "terrain_malus_multiplier": 0,
        "vision_radius": 5,
        "reward_radius": 1,
        "max_memory" :100000,
        "batch_size" :1000,
        "lr" :0.001,
        "gamma" :0.96,
        "epsilon_decay" :0.999997,
        "min_epsilon" :0.01,
        }


#Seed stats
SEED_MIN_HOOK_DURATION, SEED_MAX_HOOK_DURATION = 20, 40
SEED_MIN_SPROUT_DURATION, SEED_MAX_SPROUT_DURATION = 20, 40






if __name__ == "__main__":
    exec(open("simulation.py").read())
