import pygame, sys
from pygame.locals import *

pygame.init()
info        = pygame.display.Info()
clock       = pygame.time.Clock()

width       = info.current_w
height      = info.current_h

display     = (width, height)
screen      = pygame.display.set_mode(display, pygame.FULLSCREEN)

run         = False

clr_white   = (255, 255, 255)
clr_black   = (0, 0, 0)
clr_red     = (255, 0, 0)
clr_green   = (0, 255, 0)
clr_blue    = (0, 0, 255)

clr_default = clr_white

# def_width   = 800
# def_height  = 600
def_side    = 200

screen.fill(clr_black)

class Rectangle(pygame.Rect):
    def __init__(self, *args, **kwargs) :
        super(Rectangle, self).__init__(*args, **kwargs)  # init Rect base class
        # define additional attributes
        self.show   = True
        # self.x_speed, self.y_speed = 5, 5  # how fast it moves

    def draw(self, width=0) :
        pygame.draw.rect(screen, clr_default, self, width)

    def refresh(self) :
        self.show   = not self.show

        if self.show :
            self.draw()
        else :
            screen.fill(clr_black)

def eventLoop() :
    for event in pygame.event.get():
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE :
                pygame.quit()
                sys.exit()
            if event.key == K_SPACE :
                global run
                run = not run

def loop(forward) :
    # eventLoop()

    for event in pygame.event.get():
        if event.type == KEYDOWN :
            if event.key == K_SPACE :
                forward.refresh()
                pygame.display.update()

    # global run
    # if run :
        # forward.refresh()
        # pygame.display.update()

def run() :
    forward = Rectangle((width / 2) - (def_side / 2), (height / 4 * 1) - (def_side / 2), def_side, def_side)
    forward.draw()

    while True:  # display update loop
        loop(forward)

    # pygame.display.flip()

if __name__ == "__main__":
    run()
