from pygame.locals import *
# from threading import Thread

import pygame, sys, threading, time, os

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

clr_back    = clr_black
clr_default = clr_white

def_side    = height / 4

global_run  = True
global_lock = threading.Lock()
screen.fill(clr_back)

class Rectangle(threading.Thread):
    def __init__(self, freq) :
        threading.Thread.__init__(self)
        self.clock      = pygame.time.Clock()
        self.last_tick  = pygame.time.get_ticks()
        self.surface    = pygame.Surface((def_side, def_side))
        self.up         = 0
        self.fps        = freq * 2
        # self.play       = True

    def run(self) :
        while True :
            # self.eventLoop()
            self.loop()

    def loop(self) :
        self.clock.tick(self.fps)
        # self.last_tick = pygame.time.get_ticks()

        if (global_run) :
            if (self.up) :
                self.surface.fill(clr_default)
                # self.surface.blit(img, (0, 0))

                self.up  = 0
            else :
                self.surface.fill(clr_back)

                self.up  = 1
        else :
            self.surface.fill(clr_default)
            # self.surface.blit(img, (0, 0))

        screen.blit(self.surface, ((width - def_side) / 2, (height - def_side) / 2))
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
                # if event.key == K_SPACE :
                #     self.play = not self.play

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
                global global_run
                global_run = not global_run

def run() :
    forward         = Rectangle(10)
    forward.daemon  = True
    forward.start()

    while True :
        eventLoop()

if __name__ == "__main__":
    run()
