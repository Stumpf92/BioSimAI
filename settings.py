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

MAX_TICKS_PER_GAME = 10  # 2000
PLANT_COUNT_START = 10  
PREY_COUNT_START = 3   
HUNTER_COUNT_START = 0 
SEED_COUNT_START = 0

GRID_WIDTH = 40         #40
GRID_HEIGHT = 40      #40



####DISPLAY SETTINGS

DISPLAY_MODE = True
DISPLAY_REDUCTION_FACTOR = 20
TITLE = "BioSim"
X_OFFSET = 20
Y_OFFSET = 20

GRID_SIZE = 12

DIAGRAM_WIDTH = 300
DIAGRAM_HEIGHT = 300

FONT_SIZE = 25
BACKGROUND_COLOR = (100 , 100, 100)

FPS = 40
#TICKS_PER_SECOND = 1000

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
        "growth_rate": random.randint(20, 25)/100,
        "max_hp_multiplier": 1.1,
        "ticks_per_action": 8,
        "ticks_per_mutation": 0,
        "decay_rate": 0.01,
        "vision_radius": 1}


#Prey stats
#PREY_MIN_STARTING_HEALTH_POINTS, PREY_MAX_STARTING_HEALTH_POINTS = 60, 100
def generate_prey_heritage_stats():     
    return {
        "generation": 0,
        "min_starting_hp":60,
        "max_starting_hp":100,
        "max_hp":200,
        "reproduction_threshold": 150,
        "ticks_per_action": 6,
        "ticks_per_mutation": 0,
        "decay_rate": 0.4,
        "vision_radius": 10,
        "seeding_probability": 0.05,
        "stupid_malus": -10,
        "eating_bonus": 1000,
        "terrain_malus_multiplier": 0,}

#Hunter stats
HUNTER_MIN_STARTING_HEALTH_POINTS , HUNTER_MAX_STARTING_HEALTH_POINTS = 60, 100
def generate_hunter_heritage_stats():
    return {
        "generation": 0,
        "reproduction_threshold": 200,
        "ticks_per_action": 3,
        "ticks_per_mutation": 0,
        "decay_rate": 0.4,
        "vision_radius": 10,
        "fight_multiplier": 0.8}


#Seed stats
SEED_MIN_HOOK_DURATION, SEED_MAX_HOOK_DURATION = 20, 40
SEED_MIN_SPROUT_DURATION, SEED_MAX_SPROUT_DURATION = 20, 40


#DIAGRAM SETTINGS:

DIAGRAM_INNER_PADDING = 10




if __name__ == "__main__":
    exec(open("simulation.py").read())
