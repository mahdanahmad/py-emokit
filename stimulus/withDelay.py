from env import Env
from pygame.locals import *

import pygame, threading, sys, random

try :
    delay   = float(sys.argv[1])
except:
    delay   = 3

try :
    still   = float(sys.argv[2])
except:
    still   = 0.1

pygame.init()
info        = pygame.display.Info()
clock       = pygame.time.Clock()
env         = Env(info.current_w, info.current_h)

screen      = pygame.display.set_mode(env.getResolution(), pygame.FULLSCREEN)
clr_back    = env.getColor('black')
clr_default = env.getColor('white')

screen.fill(clr_back)
pygame.display.update()

avail_state = ['stop', 'left', 'right', 'forward']

position    = env.getRectPos()
updatable   = position + env.getRectSize()

run         = True
fps         = 10

def coverBack() :
    surface = pygame.Surface(env.getRectSize())
    surface.fill(clr_back)

    screen.blit(surface, position)

def drawRectangle(img) :
    surface = pygame.Surface(env.getRectSize())
    surface.fill(clr_default)
    surface.blit(img, (0, 0))

    screen.blit(surface, position)

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

def run() :
    image       = env.getRectIMG(random.choice(avail_state))
    counter     = 0
    show_image  = 0

    while True :
        eventLoop()
        clock.tick(fps)

        counter += 1
        if (run) :
            if (show_image) :
                drawRectangle(image)
                if (counter == (still * fps)) :
                    image       = env.getRectIMG(random.choice(avail_state))
                    counter     = 0
                    show_image  = 0
            else :
                coverBack()
                if (counter == ((delay - still) * fps)) :
                    counter     = 0
                    show_image  = 1
        else :
            coverBack()
            counter     = 0
            show_image  = 0

        pygame.display.update(updatable)
        # show_image  = not show_image

if __name__ == "__main__":
    run()
