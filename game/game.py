import pygame
import time
import random
import numpy as np

pygame.init()

velocity = 2

display_width = 810
display_height = 510

arena_x = 805
arena_y = 505

bot_scale = 0.1125

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('ERA-IITK')

# carImg = pygame.image.load('racecar.png')

# carImg = pygame.transform.rotozoom(carImg, 90, 1)

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False

x = 5
y = 455

bot_height=50
bot_width=25

x_center = x+bot_width/2
y_center = y+bot_height/2

x_change = 0
y_change = 0

screen = pygame.display.set_mode((display_width, display_height))
# carImg = pygame.draw.circle(screen , black, (x, y), bot_width)

direction = 0

class GameState:
    
    def frame_step(self, input_actions):
        terminal=False
        reward=0.1
        
        #input_actions[0]==1:stop
        #input_actions[1]==1:move_down
        #input_actions[2]==1:move_right
        #input_actions[3]==1:move_left
        #input_actions[4]==1:rev_bot_dim
        #input_actions[5]==1:move_up
        if sum(input_actions)!=1:
            print("Multiple actions ")
        else:
            if input_actions[0]==1:
                self.stop()
            elif input_actions[1]==1:
                self.move_down()
            elif input_actions[2]==1:
                self.move_right()
            elif input_actions[3]==1:
                self.move_left()
            elif input_actions[4]==1:
                self.rev_bot_dim()
            elif input_actions[5]==1:
                self.move_up()
                
            if self.boundary():
                reward=-1
                terminal=True
                
            # x+= x_change
            # y+= y_change
            
            self.__init__()
            # self.car(x,y)
            return gameDisplay, reward, terminal
        
    def things(self, thingx, thingy, thingw, thingh, color):
        pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

    def rev_bot_dim(self): #rotate bot 
        global bot_height
        global bot_width
        
        bot_width,bot_height = bot_height,bot_width

    def car(self,x,y): #display  car
        global carImg
        global black
        
        carImg = pygame.draw.rect(gameDisplay, black, [x, y, bot_width, bot_height])
            
    def stop(self):
        global x_change, y_change
        
        x_change=0
        y_change=0
    def move_up(self):
        global x_change
        global y_change
        global velocity
        
        x_change = 0
        y_change = -velocity
        
    def move_down(self):
        global x_change
        global y_change
        global velocity
        
        x_change = 0
        y_change = velocity
        
    def move_right(self):
        global x_change
        global y_change
        global velocity
        
        x_change = velocity
        y_change = 0

    def move_left(self):
        global x_change
        global y_change
        global velocity
        
        x_change = -velocity
        y_change = 0
        
    def boundary(self):
        global x_change
        global y_change
        global x
        global y
        
        
        if (x+x_change)<5 or (x+bot_width+x_change)>805 or (y+bot_height+y_change)>505 or (y+y_change)<5:
            x_change=0
            y_change=0
            return True
            
        if ((x+bot_width+x_change)>455 and (x+x_change)<480) and (y+y_change)<105:
            x_change=0
            y_change=0
            return True
            
        if ((x+bot_width+x_change)>145 and (x+x_change)<170) and (y+y_change)<365 and (y+bot_height+y_change)>265:
            x_change=0
            y_change=0
            return True
            
        if ((x+bot_width+x_change)>640 and (x+x_change)<665) and (y+y_change)<245 and (y+bot_height+y_change)>145:
            x_change=0
            y_change=0
            return True
            
        if ((x+bot_width+x_change)>330 and (x+x_change)<355) and (y+y_change)<505 and (y+bot_height+y_change)>405:
            x_change=0
            y_change=0
            return True
            
        if ((x+bot_width+x_change)>125 and (x+x_change)<225) and (y+y_change)<130 and (y+bot_height+y_change)>105:
            x_change=0
            y_change=0
            return True
            
        if ((x+bot_width+x_change)>355 and (x+x_change)<455) and (y+y_change)<267.5 and (y+bot_height+y_change)>242.5:
            x_change=0
            y_change=0
            return True
            
        if ((x+bot_width+x_change)>585 and (x+x_change)<685) and (y+y_change)<430 and (y+bot_height+y_change)>405:
            x_change=0
            y_change=0
            return True
        
        return False
    def __init__(self):
        
        global crashed, direction, bot_height, bot_width, x, y, x_change, y_change, x_center, y_center, black, white, arena_x, arena_y, display_height, display_width
        
        # x_change=0
        # y_change=0
        
        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_LEFT:
                #         direction=4
                #     elif event.key == pygame.K_RIGHT:
                #         direction=3
                #     elif event.key == pygame.K_UP:
                #         direction = 1
                #     elif event.key == pygame.K_DOWN:
                #         direction = 2
                        
                #     if event.key == pygame.K_m:
                #         self.rev_bot_dim()
                #         if(self.boundary()):
                #             self.rev_bot_dim()                    
                
                # elif event.type == pygame.KEYUP:
                #     direction=0

            gameDisplay.fill(white)
                
            self.things(0, 0, display_width, display_height, black)
            self.things(5, 5, 800, 500, white)
            
            self.things(455, 5, 25, 100, black)
            self.things(145, 265, 25, 100, black)
            self.things(640, 145, 25, 100, black)
            self.things(330, 405, 25, 100, black)
            
            self.things(125, 105, 100, 25, black)
            self.things(355, 242.5, 100, 25, black)
            self.things(585, 405, 100, 25, black)
            
                
                
            # if direction == 1:
            #     self.move_up()
            # elif direction == 2:
            #     self.move_down()
            # elif direction == 3:
            #     self.move_right()
            # elif direction == 4:
            #     self.move_left()
            # elif direction == 0:
            #     x_change=0
            #     y_change=0
            
            # self.boundary() 

            x+= x_change
            y+= y_change
            
            self.car(x,y)

            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        quit()
        
if __name__ == "__main__":
    GameState()