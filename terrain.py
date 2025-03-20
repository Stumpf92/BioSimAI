import settings
import numpy as np
np.random.seed(settings.SEED)
import random
random.seed(settings.SEED)
import opensimplex

class Terrain():

    def __init__(self):
        self.terrain_map = np.ones([settings.GRID_HEIGHT, settings.GRID_WIDTH])
        if settings.TERRAIN_ACTIVATION_MODE == True:
            self.generate_hightmap()
            if settings.RIVER_ACTIVATION_MODE == True:
                self.generate_river()
        



    def generate_hightmap(self):
        # generiert eine Höhenkarte
        opensimplex.seed(settings. TERRAIN_SEED)
        for x in range(settings.GRID_WIDTH):
            for y in range(settings.GRID_HEIGHT):
                self.terrain_map[x,y] = int((opensimplex.noise2(x/settings.TERRAIN_NOISE_ZOOM, y/settings.TERRAIN_NOISE_ZOOM)+1)*(settings.TERRAIN_MAX_HEIGHT)/2)

    def generate_river(self):
        # generiert einen Fluss
        starting_tile = random.choice(self.find_lowest_edge_tiles())[1]
        print(starting_tile)
        self.terrain_map[starting_tile[0],starting_tile[1]] = -1
        pass
    
    def find_lowest_edge_tiles(self):
        # findet den niegrigsten Tile am Rand der Karte
        values_and_tiles = []
        for x in range(settings.GRID_WIDTH):
            values_and_tiles.append([self.terrain_map[x,0], [x,0]])
            values_and_tiles.append([self.terrain_map[x, settings.GRID_HEIGHT-1], [x, settings.GRID_HEIGHT-1]])
        for y in range(settings.GRID_HEIGHT):
            values_and_tiles.append([self.terrain_map[0,y], [0,y]])
            values_and_tiles.append([self.terrain_map[settings.GRID_WIDTH-1, y], [settings.GRID_WIDTH-1, y]])

        values_and_tiles = sorted(values_and_tiles, key = lambda x: x[0])
            
        print([tiles for tiles in values_and_tiles if tiles[0] == values_and_tiles[0][0]])
        return [tiles for tiles in values_and_tiles if tiles[0] == values_and_tiles[0][0]]


if __name__ == "__main__":
    exec(open("main.py").read())
