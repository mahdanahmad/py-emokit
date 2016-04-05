import pygame, sys, thread, time
from pygame.locals import *

pygame.init()
info        = pygame.display.Info()
clock       = pygame.time.Clock()

width       = info.current_w
height      = info.current_h

display     = (width, height)
screen      = pygame.display.set_mode(display, pygame.FULLSCREEN)

clr_white   = (255, 255, 255)
clr_black   = (0, 0, 0)
clr_red     = (255, 0, 0)
clr_green   = (0, 255, 0)
clr_blue    = (0, 0, 255)

clr_default = clr_white

def_side    = height / 4

global_fps  = 60
rect_fps    = [7.5, 10, 12, 15]
# rect_fps    = [1, 1, 2, 2]

screen.fill(clr_black)

class Rectangle(pygame.Rect):
    def __init__(self) :
        self.clock      = pygame.time.Clock()
        self.last_tick  = pygame.time.get_ticks()

        self.run    = True

        top_x       = (width / 4) * 2 - (def_side / 2)
        top_y       = (height / 4) * 1 - (def_side / 2)
        mid_x       = (width / 4) * 2 - (def_side / 2)
        mid_y       = (height / 4) * 3 - (def_side / 2)
        rgt_x       = (width / 4) * 3 - (def_side / 2)
        rgt_y       = (height / 4) * 3 - (def_side / 2)
        lft_x       = (width / 4) * 1 - (def_side / 2)
        lft_y       = (height / 4) * 3 - (def_side / 2)

        self.pos    = [(top_x, top_y), (mid_x, mid_y), (rgt_x, rgt_y), (lft_x, lft_y)]
        self.rect   = []

        count       = len(self.pos)
        while (count > 0):
           count    = count - 1

           temp     = pygame.Surface((def_side, def_side))
           temp.fill(clr_default)

           self.rect.append(temp)

        self.periode    = []
        self.count      = [0, 0, 0, 0]
        self.alpha      = [255, 255, 255, 255]

        for val in rect_fps:
            self.periode.append(global_fps / val)

        start_time      = time.time()
        while True :
            self.loop()

    def loop(self) :
        self.eventLoop()

        self.clock.tick_busy_loop(global_fps)
        self.last_tick = pygame.time.get_ticks()

        # print self.count

        screen.fill(clr_black)
        if (self.run) :
            for key, val in enumerate(self.periode):
                if (self.count[key] < val / 2) :
                    self.alpha[key] = 255
                else :
                    self.alpha[key] = 0

                self.count[key] = self.count[key] + 1
                if (self.count[key] == val) : self.count[key] = 0

        else :
            self.count  = [0, 0, 0, 0]
            self.alpha  = [255, 255, 255, 255]

        for key, value in enumerate(self.rect) :
            value.set_alpha(self.alpha[key])
            screen.blit(value, self.pos[key])

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
    Rectangle();

if __name__ == "__main__":
    run()
