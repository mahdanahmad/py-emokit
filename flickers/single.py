import pygame, sys, thread, time
from pygame.locals import *

pygame.init()
info        = pygame.display.Info()
clock       = pygame.time.Clock()

width       = info.current_w
height      = info.current_h

display     = (width, height)
screen      = pygame.display.set_mode(display, pygame.FULLSCREEN)

try :
    fps     = int(sys.argv[1])
except:
    fps     = 15

clr_white   = (255, 255, 255)
clr_black   = (0, 0, 0)
clr_red     = (255, 0, 0)
clr_green   = (0, 255, 0)
clr_blue    = (0, 0, 255)

clr_default = clr_white

def_side    = 200

screen.fill(clr_black)

class Rectangle(pygame.Rect):
    def __init__(self, fps) :
        self.clock      = pygame.time.Clock()
        self.last_tick  = pygame.time.get_ticks()

        self.run    = True

        self.fps    = fps

        self.rect   = pygame.Surface((def_side, def_side))
        self.rect.fill(clr_default)

        self.alpha  = 0

        while True :
            self.loop()

    def loop(self) :
        self.eventLoop()

        self.last_tick = pygame.time.get_ticks()
        self.clock.tick(self.fps)

        screen.fill(clr_black)
        if (self.run) :
            if self.alpha == 0 :
                self.alpha  = 255
            elif self.alpha == 255 :
                self.alpha  = 0
        else :
            self.alpha = 255

        self.rect.set_alpha(self.alpha)
        screen.blit(self.rect, ((width - def_side) / 2, (height - def_side) / 2))

        pygame.display.update()

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
