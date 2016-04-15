from env import Env
from pygame.locals import *
from rectangle import Rectangle
import pygame, threading, sys

pygame.init()
info        = pygame.display.Info()
clock       = pygame.time.Clock()
env         = Env(info.current_w, info.current_h)

screen      = pygame.display.set_mode(env.getResolution(), pygame.FULLSCREEN)
clr_back    = env.getColor('black')
clr_default = env.getColor('white')

screen.fill(clr_back)

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
    forward = Rectangle()
    forward.start(env.getStop(), env.getRun())

    while True :
        eventLoop()
        clock.tick(env.getFPS())

if __name__ == "__main__":
    run()
