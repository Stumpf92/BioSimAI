import random

####SIMULATION SETTINGS

MAX_GAMES_PER_SIMULATION = 10000000
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001    # 0.001
GAMMA = 0.9
EPSILON_DECAY = 0.999995     #0.99995
MIN_EPSILON = 0.01

###GAME SETTINGS

MAX_TICKS_PER_GAME = 1000  # 2000
PLANT_COUNT_START = 20  
PREY_COUNT_START = 10   
HUNTER_COUNT_START = 5 
SEED_COUNT_START = 3

GRID_WIDTH = 35         #40
GRID_HEIGHT = 35      #40



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
#PLANT_MIN_STARTING_HEALTH_POINTS, PLANT_MAX_STARTING_HEALTH_POINTS = 5, 50
def generate_plant_heritage_stats():
    return {
        "generation": 0,
        "min_starting_hp":5,
        "max_starting_hp":50,
        "max_hp":100,
        "reproduction_threshold": 80,
        "growth_rate": random.randint(40, 50)/100,
        "max_hp_multiplier": 1.1,
        "ticks_per_action": 8,
        "ticks_per_mutation": 0,
        "decay_rate": 0.001,
        "vision_radius": 1,
        "seeding_max_timer": 10}


#Prey stats
#PREY_MIN_STARTING_HEALTH_POINTS, PREY_MAX_STARTING_HEALTH_POINTS = 60, 100
def generate_prey_heritage_stats():     
    return {
        "generation": 0,
        "min_starting_hp":30,
        "max_starting_hp":120,
        "max_hp":250,
        "reproduction_threshold": 230,
        "decay_rate": 0.002,
        "vision_radius": 10,
        "seeding_probability": 0.05,
        "stupid_malus": -50,
        "eating_bonus": 100,
        "getting_closer_bonus": 20,
        "terrain_malus_multiplier": 0,
        "seeding_chance": 0.1,
        "seeding_max_timer": 10}

#Hunter stats
HUNTER_MIN_STARTING_HEALTH_POINTS , HUNTER_MAX_STARTING_HEALTH_POINTS = 60, 100
def generate_hunter_heritage_stats():
    return {
        "generation": 0,
        "min_starting_hp":80,
        "max_starting_hp":150,
        "max_hp":700,
        "reproduction_threshold": 600,
        "decay_rate": 0.007,
        "vision_radius": 10,
        "seeding_probability": 0.05,
        "stupid_malus": -50,
        "eating_bonus": 100,
        "getting_closer_bonus": 20,
        "terrain_malus_multiplier": 0,}


#Seed stats
SEED_MIN_HOOK_DURATION, SEED_MAX_HOOK_DURATION = 20, 40
SEED_MIN_SPROUT_DURATION, SEED_MAX_SPROUT_DURATION = 20, 40






if __name__ == "__main__":
    exec(open("simulation.py").read())
