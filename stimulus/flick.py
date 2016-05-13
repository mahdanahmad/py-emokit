from stimulus_env import Env
from pygame.locals import *

import pygame, threading, os, sys

pygame.init()
info        = pygame.display.Info()
clock       = pygame.time.Clock()
env         = Env(info.current_w, info.current_h)

screen      = pygame.display.set_mode(env.getResolution(), pygame.FULLSCREEN)
clr_back    = env.getColor('black')
clr_default = env.getColor('white')

global_lock = threading.Lock()

screen.fill(clr_back)

avail_state = ['stop', 'left', 'right', 'forward']

class Rectangle(threading.Thread):
    def __init__(self, freq, pos, img, name='Unnamed', ) :
        threading.Thread.__init__(self)
        self.clock      = pygame.time.Clock()
        self.surface    = pygame.Surface(env.getRectSize())
        self.up         = 0
        self.name       = name
        self.image      = img
        self.delay      = 1000 / (freq * 2)

        self.pos        = pos
        self.rect       = pos + env.getRectSize()

        # print self.delay
        # self.count      = 0
        # self.init_tick  = pygame.time.get_ticks()
    def run(self) :
        while True :
            if env.getStop() :
                return
            else :
                self.loop()

    def loop(self) :
        self.clock.tick()

        if (env.getRun()) :
            if (self.up) :
                self.up  = 0
                self.surface.fill(clr_default)
                if self.image is not None : self.surface.blit(self.image, (0, 0))

            else :
                self.up  = 1
                self.surface.fill(clr_back)

        else :
            self.up  = 0
            self.surface.fill(clr_default)
            if self.image is not None : self.surface.blit(self.image, (0, 0))

        global_lock.acquire()
        try:
            screen.blit(self.surface, self.pos)
            pygame.display.update(self.rect)
        finally:
            global_lock.release()

        # self.count += 1
        # print self.name + ' => ' + str(self.count) + ' => ' + str(self.clock.get_time()) + " => " + str(self.clock.get_fps()) + " fps => " + str((pygame.time.get_ticks() - self.init_tick) / 1000)
        # print self.name

        pygame.time.wait(self.delay)

def eventLoop() :
    for event in pygame.event.get():
        if event.type == QUIT :
            env.killStop()
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE :
                env.killStop()
                pygame.quit()
                sys.exit()
            if event.key == K_SPACE :
                env.changeRun()

def run() :
    for val in avail_state :
        rect    = Rectangle(env.getRectFreq(val), env.getRectPos(val), env.getRectIMG(val), val)
        rect.start()

    while True :
        eventLoop()
        clock.tick(env.getFPS())

if __name__ == "__main__":
    run()
