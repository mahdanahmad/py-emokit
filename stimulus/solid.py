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

avail_state = ['stop', 'left', 'right', 'forward']

def drawRectangle(pos, img) :
    surface = pygame.Surface(env.getRectSize())
    surface.fill(clr_default)
    surface.blit(img, (0, 0))

    screen.blit(surface, pos)

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
    for val in avail_state : drawRectangle(env.getRectPos(val), env.getIMG(val))

    pygame.display.flip()

    while True :
        eventLoop()
        clock.tick(env.getFPS())

if __name__ == "__main__":
    run()
