import pygame as pg
import settings
from plant import Plant
from prey import Prey
import os

class Display:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (1000,122)
        pg.init()
        pg.font.init()
        self.font = pg.font.Font(None,settings.FONT_SIZE)
        self.screen = pg.display.set_mode(((settings.GRID_WIDTH*settings.GRID_SIZE+(2*settings.X_OFFSET)+settings.TEXT_FIELD_WIDTH),
                                           max(settings.GRID_HEIGHT*settings.GRID_SIZE+(2*settings.Y_OFFSET), settings.TEXT_FIELD_HEIGHT)))
        pg.display.set_caption('BioSim')
        self.clock = pg.time.Clock()

        self.queue_of_valuable_informations = []

        self.drawing_mode = False
          
    def save(self,all_valuable_informations):
        # if all_valuable_informations[-1]["mean_score"] > all_valuable_informations[-1]["score"]:
        #     self.queue_of_valuable_informations.append(all_valuable_informations)

        if all_valuable_informations[-1]["record_mode"] == True:
            self.queue_of_valuable_informations.append(all_valuable_informations)
        elif len(self.queue_of_valuable_informations) < 2:
            self.queue_of_valuable_informations.append(all_valuable_informations)


    def render(self):
        self.drawing_mode = True
        oldest_valuable_informations = self.queue_of_valuable_informations.pop(0)
        for i in oldest_valuable_informations:       
            n_games = i["n_games"]
            record = i["record"]
            mean_score = i["mean_score"]
            frame_iteration = i["frame_iteration"]
            reward = i["reward"]
            game_over = i["game_over"]
            score = i["score"]
            map_per_tick = i["map_per_tick"]
            plant_count = i["plant_count"]
            prey_count = i["prey_count"]
            action = i["action"]
            terrain = i["terrain"]
            epsilon = i["epsilon"]

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False


            self.screen.fill(settings.BACKGROUND_COLOR)
            pg.draw.rect(self.screen, (0,0,0), (settings.X_OFFSET-1, settings.Y_OFFSET-1, settings.GRID_WIDTH*settings.GRID_SIZE+2, settings.GRID_HEIGHT*settings.GRID_SIZE+2),width=1)

            self.render_text("n_game:  "+ str(int(n_games)), (0,0,0), (2*settings.X_OFFSET+(settings.GRID_WIDTH*settings.GRID_SIZE),settings.Y_OFFSET+5))
            self.render_text("record:  "+ str(int(record)), (0,0,0), (2*settings.X_OFFSET+(settings.GRID_WIDTH*settings.GRID_SIZE),settings.Y_OFFSET+25))
            self.render_text("mean:  "+ str(int(mean_score)), (0,0,0), (2*settings.X_OFFSET+(settings.GRID_WIDTH*settings.GRID_SIZE),settings.Y_OFFSET+45))
            self.render_text("frame:  "+ str(int(frame_iteration)), (0,0,0), (2*settings.X_OFFSET+(settings.GRID_WIDTH*settings.GRID_SIZE),settings.Y_OFFSET+105))
            self.render_text("reward:  "+ str(int(reward)), (0,0,0), (2*settings.X_OFFSET+(settings.GRID_WIDTH*settings.GRID_SIZE),settings.Y_OFFSET+125))
            self.render_text("score:  "+ str(int(score)), (0,0,0), (2*settings.X_OFFSET+(settings.GRID_WIDTH*settings.GRID_SIZE),settings.Y_OFFSET+145))
            self.render_text("plant:  "+ str(int(plant_count)), (0,0,0), (2*settings.X_OFFSET+(settings.GRID_WIDTH*settings.GRID_SIZE),settings.Y_OFFSET+165))
            self.render_text("prey:  "+ str(int(prey_count)), (0,0,0), (2*settings.X_OFFSET+(settings.GRID_WIDTH*settings.GRID_SIZE),settings.Y_OFFSET+185)) 
            self.render_text("epsilon:  "+ str(round(epsilon,3)), (0,0,0), (2*settings.X_OFFSET+(settings.GRID_WIDTH*settings.GRID_SIZE),settings.Y_OFFSET+205))



            for x in range(settings.GRID_WIDTH):
                for y in range(settings.GRID_HEIGHT):

                    color = (int(settings.TERRAIN_BASE_COLOR[0]+terrain[x,y]*settings.TERRAIN_COLOR_STEP),
                              int(settings.TERRAIN_BASE_COLOR[1]+terrain[x,y]*settings.TERRAIN_COLOR_STEP),
                                int(settings.TERRAIN_BASE_COLOR[2]+terrain[x,y]*settings.TERRAIN_COLOR_STEP))
                    pg.draw.rect(self.screen, color, (x*settings.GRID_SIZE+settings.X_OFFSET, y*settings.GRID_SIZE+settings.Y_OFFSET, settings.GRID_SIZE, settings.GRID_SIZE))
                    
                    if isinstance(map_per_tick[x,y], Plant):
                        pg.draw.circle(self.screen, (0, 255, 0), (x*settings.GRID_SIZE+settings.X_OFFSET+settings.GRID_SIZE//2, y*settings.GRID_SIZE+settings.Y_OFFSET+settings.GRID_SIZE//2), settings.GRID_SIZE//2)
                    elif isinstance(map_per_tick[x,y], Prey):
                        pg.draw.circle(self.screen, (0, 0, 255), (x*settings.GRID_SIZE+settings.X_OFFSET+settings.GRID_SIZE//2, y*settings.GRID_SIZE+settings.Y_OFFSET+settings.GRID_SIZE//2), settings.GRID_SIZE//2)
                

            pg.display.flip()
            self.clock.tick(settings.FPS) 
        
        self.drawing_mode = False

    def render_text(self, text, color, pos):
        text = self.font.render(text, True, color)
        self.screen.blit(text, pos)


if __name__ == "__main__":
    exec(open("simulation.py").read())
