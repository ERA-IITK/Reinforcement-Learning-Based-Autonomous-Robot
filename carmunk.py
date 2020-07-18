import pygame
import time
import random
import numpy as np
import math


velocity = 10

display_width = 820
display_height = 520

arena_x = 810
arena_y = 510

bot_scale = 0.1125
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('ERA-IITK')

obstacle_length=100
obstacle_width=25

black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

bot_height=60
bot_width=45

# clock = pygame.time.Clock()

crashed = False

x = 5
y = 515-bot_width

x_change = 0
y_change = 0

direction = 0
class GameState:
    def draw_rect(self,width, height, point_x, point_y, color):
        pygame.draw.rect(gameDisplay, color, [point_x, point_y, height, width])
        
    def movement(self):
        global direction, x_change, y_change
        
        if direction==1:
            y_change=-velocity
            x_change=0
        elif direction==2:
            y_change=velocity
            x_change=0
        elif direction==3:
            x_change=velocity
            y_change=0
        elif direction==4:
            x_change=-velocity
            y_change=0
        elif direction==0:
            x_change=0
            y_change=0
        
    def botInObstacle(self):
        global x, y
        obstacle_x = [5, 815-470, 815-470, 715, 155, 815-230, 155, 815-175]
        obstacle_y = [105, 105, 515-125, 515-125, 247.5, 247.5, 515-100, 5]
        obstacle_length  = [100, 100, 100, 100, 80, 80, 25, 25]
        obstacle_width = [25, 25, 25, 25, 25, 25, 100, 100]
        for i in range(8):
            if (obstacle_x[i] < x + 60 < obstacle_x[i] + obstacle_length[i] or obstacle_x[i] < x < obstacle_length[i] + obstacle_x[i]) and (obstacle_y[i] < y + 45 < obstacle_y[i] + obstacle_width[i] or obstacle_y[i] < y < obstacle_width[i] + obstacle_y[i]):
                return 1
        if (x + 60 < 820 and x>0 and y >0 and y + 45<520):
            return 0
        else : return 1
        
    def botInBuff(self):
        global x, y
        obstacle_x = [ 815-437]
        obstacle_y = [ 515-75]
        obstacle_length  = [54]
        obstacle_width = [48]
        for i in range(len(obstacle_x)):
            if (obstacle_x[i] < x + 60 < obstacle_x[i] + obstacle_length[i] or obstacle_x[i] < x < obstacle_length[i] + obstacle_x[i]) and (obstacle_y[i] < y + 45 < obstacle_y[i] + obstacle_width[i] or obstacle_y[i] < y < obstacle_width[i] + obstacle_y[i]):
                return 1
            
    def botInDeBuff(self):
        global x, y
        obstacle_x = [168, 815-217,815-437, 815-77]
        obstacle_y = [515-217.5, 174.5,32,312]
        obstacle_length  = [54, 54,54,54]
        obstacle_width = [48, 48,48,48]
        for i in range(4):
            if (obstacle_x[i] < x + 60 < obstacle_x[i] + obstacle_length[i] or obstacle_x[i] < x < obstacle_length[i] + obstacle_x[i]) and (obstacle_y[i] < y + 45 < obstacle_y[i] + obstacle_width[i] or obstacle_y[i] < y < obstacle_width[i] + obstacle_y[i]):
                return 1

    def draw_car(self):
        global x, y
        pygame.draw.rect(gameDisplay, black, [x, y, bot_height, bot_width])
        
    def frame_step(self, action):
        pygame.event.pump()
        global crashed, x, y, x_change, y_change,direction
        # while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                        
        direction=action
        #action0 stop action1 up action2 down action3 right action4 left
                
        self.movement()
        x=x+x_change
        y=y+y_change        
                    
        gameDisplay.fill(white)
                
        self.draw_rect(display_height, display_width, 0, 0, black)
        self.draw_rect(arena_y, arena_x, 5, 5, white)
        
        self.draw_rect(obstacle_width, obstacle_length, 5, 105, black)
        self.draw_rect(obstacle_width, obstacle_length, 815-470, 105, black)
        self.draw_rect(obstacle_width, obstacle_length, 815-470, 515-125, black)
        self.draw_rect(obstacle_width, obstacle_length, 715, 515-125, black)
        
        self.draw_rect(obstacle_width, obstacle_length-20, 155, 247.5, black)
        self.draw_rect(obstacle_width, obstacle_length-20, 815-230, 247.5, black)
        
        self.draw_rect(48, 54, 28, 515-360, yellow)
        self.draw_rect(48, 54, 168, 515-217.5, red)       
        self.draw_rect(48, 54, 815-437, 515-75, green)    
        self.draw_rect(48, 54, 815-437, 32, blue)
        self.draw_rect(48, 54, 815-77, 515-(515-312), blue)
        self.draw_rect(48, 54, 815-217, 174.5, red)
        
        self.draw_rect(obstacle_length, obstacle_width, 155, 515-100, black)
        self.draw_rect(obstacle_length, obstacle_width, 815-175, 5, black)
        
        pygame.draw.polygon(gameDisplay, black, ((410-21.2,260),(410,260+21.2),(410+21.2,260),(410,260-21.2)))
            
        self.draw_car()
        self.botInObstacle()
            
        pygame.display.update()
        # clock.tick(60)
        term=0
        reward=-1
        if self.botInObstacle() :
            term=1
            reward=-100
            state=(5,515-bot_width)
            x,y=state
        elif self.botInDeBuff():
            term=0
            reward=-150
            state=(x,y)
        elif self.botInBuff():
            term=2
            reward=500
            state=(5,515-bot_width)
            x,y=state
        else:
            term=0
            reward=-1
            state=(x,y)
        # pygame.quit()
        # quit()
        myret=(reward,state,term)
        # print(myret)
        return myret

    
if __name__ == "__main__":
    game_state = GameState()
    while True:
        game_state.frame_step(1)