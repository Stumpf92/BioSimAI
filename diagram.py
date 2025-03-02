import pygame as pg
import settings

class Diagram():
    def __init__(self, surface, topleft_x, topleft_y, width, height, text):
        self.surface = surface
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.width = width
        self.height = height
        self.text = text

        self.scale_width = 10

        self.font = pg.font.SysFont("Arial", 15)

        self.top_y_axis = (self.topleft_x+settings.DIAGRAM_INNER_PADDING, self.topleft_y+settings.DIAGRAM_INNER_PADDING)
        self.bot_y_axis = (self.topleft_x+settings.DIAGRAM_INNER_PADDING, self.topleft_y+self.height-1*settings.DIAGRAM_INNER_PADDING)

        #([[1,2,3,4,5,6],[1,1,2,2,3,1]])

    
    def draw(self, data):
        x_min = min(data[0])
        x_max = max(data[0])
        y_min = min(min(data[1]),0)
        y_max = max(data[1])

        x_per_px = (x_max-x_min)/((self.topleft_x+self.width-1*settings.DIAGRAM_INNER_PADDING)-self.topleft_x+settings.DIAGRAM_INNER_PADDING)
        y_per_px = (y_max-y_min)/(self.bot_y_axis[1]-self.top_y_axis[1])

        if y_min == 0:
            self.origin = (self.topleft_x+settings.DIAGRAM_INNER_PADDING, self.topleft_y+self.height-1*settings.DIAGRAM_INNER_PADDING)
        else:
            self.origin = (self.topleft_x+settings.DIAGRAM_INNER_PADDING, self.topleft_y+self.height-1*settings.DIAGRAM_INNER_PADDING-y_per_px*y_min)


        self.right_x_axis = (self.topleft_x+self.width-1*settings.DIAGRAM_INNER_PADDING, self.origin[1])
        pg.draw.rect(self.surface, (200,200,200), (self.topleft_x-1, self.topleft_y-1, self.width+2, self.height+2),border_radius=10)
        pg.draw.rect(self.surface, (0,0,0), (self.topleft_x-1, self.topleft_y-1, self.width+2, self.height+2),width=1, border_radius=10)

        self.render_text((self.topleft_x + self.width//3, self.topleft_y+1), self.text, (0,0,0))

        pg.draw.line(self.surface, (0,0,0), self.top_y_axis, self.bot_y_axis, width=2)
        pg.draw.line(self.surface, (0,0,0), self.origin, self.right_x_axis, width=2)

        for i in range(len(data[0])):
            self.render_dot((data[0][i]/x_per_px,self.bot_y_axis[1]-data[1][i]/y_per_px))
        



    def render_text(self, pos, text, color):
        text = self.font.render(text, True, color)
        self.surface.blit(text, pos)
    
    def render_dot(self, pos):
        pg.draw.circle(self.surface, (0,0,0), pos, 6)



if __name__ == "__main__":
    exec(open("simulation.py").read())

