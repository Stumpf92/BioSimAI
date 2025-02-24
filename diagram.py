import pygame as pg
import settings

class Diagram():
    def __init__(self, surface, topleft_x, topleft_y, width, height):
        self.surface = surface
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.width = width
        self.height = height

        self.scale_width = 10

        self.top_y_axis = (self.topleft_x+settings.DIAGRAM_INNER_PADDING, self.topleft_y+settings.DIAGRAM_INNER_PADDING)
        self.bot_y_axis = (self.topleft_x+settings.DIAGRAM_INNER_PADDING, self.topleft_y+self.height-1*settings.DIAGRAM_INNER_PADDING)

    
    def draw(self):
        self.origin = (self.topleft_x+settings.DIAGRAM_INNER_PADDING, self.topleft_y+100)
        self.right_x_axis = (self.topleft_x+self.width-1*settings.DIAGRAM_INNER_PADDING, self.origin[1])
        pg.draw.rect(self.surface, (0,0,0), (self.topleft_x-1, self.topleft_y-1, self.width+2, self.height+2),width=1)
        pg.draw.line(self.surface, (0,0,0), self.top_y_axis, self.bot_y_axis, width=1)
        pg.draw.line(self.surface, (0,0,0), self.origin, self.right_x_axis, width=1)





if __name__ == "__main__":
    exec(open("simulation.py").read())

