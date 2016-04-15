from env import Env
from pygame.locals import *

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
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE :
                pygame.quit()
                sys.exit()

def run() :
    while True :
        eventLoop()
        clock.tick(env.getFPS())

if __name__ == "__main__":
    run()
