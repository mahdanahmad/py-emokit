import pygame, sys, thread, time, os
from pygame.locals import *

pygame.init()
info        = pygame.display.Info()
clock       = pygame.time.Clock()

width       = info.current_w
height      = info.current_h

display     = (width, height)
screen      = pygame.display.set_mode(display, pygame.FULLSCREEN)

fps         = 12

clr_white   = (255, 255, 255)
clr_black   = (0, 0, 0)
clr_red     = (255, 0, 0)
clr_green   = (0, 255, 0)
clr_blue    = (0, 0, 255)

clr_back    = clr_black
clr_default = clr_white

def_side    = height / 4

screen.fill(clr_back)

img_loc     = os.path.join("images", "circle-stop.png")
img         = pygame.image.load(img_loc)
img         = pygame.transform.scale(img, (def_side, def_side))

class Rectangle():
    def __init__(self, fps) :
        self.clock      = pygame.time.Clock()
        self.last_tick  = pygame.time.get_ticks()
        self.rect       = pygame.Surface((def_side, def_side))
        self.up         = 0
        self.run        = True
        self.fps        = fps * 2

        while True :
            self.loop()

    def loop(self) :
        self.eventLoop()

        self.clock.tick(self.fps)
        # self.last_tick = pygame.time.get_ticks()

        if (self.run) :
            if (self.up) :
                self.rect.fill(clr_default)
                # self.rect.blit(img, (0, 0))

                self.up  = 0
            else :
                self.rect.fill(clr_back)

                self.up  = 1
        else :
            self.rect.fill(clr_default)
            self.rect.blit(img, (0, 0))

        # self.rect.set_alpha(self.alpha)
        screen.blit(self.rect, ((width - def_side) / 2, (height - def_side) / 2))

        pygame.display.update(((width - def_side) / 2, (height - def_side) / 2, def_side, def_side))

    def eventLoop(self) :
        for event in pygame.event.get():
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN :
                if event.key == K_ESCAPE :
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE :
                    self.run = not self.run
def run() :
    forward = Rectangle(fps)

if __name__ == "__main__":
    run()
