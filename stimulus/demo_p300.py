import pygame, sys, thread, time, os, random
from pygame.locals import *
from env import Env

pygame.init()
info        = pygame.display.Info()
clock       = pygame.time.Clock()
env         = Env(info.current_w, info.current_h)

width       = info.current_w
height      = info.current_h

display     = (width, height)
screen      = pygame.display.set_mode(display, pygame.FULLSCREEN)

up          = 0
fps         = 10
run         = True

counter     = 0
max_ctr     = 29

screen      = pygame.display.set_mode(env.getResolution(), pygame.FULLSCREEN)
# screen      = pygame.display.set_mode([700, 500])
clr_back    = env.getColor('black')
clr_yellow  = env.getColor('yellow')
clr_default = env.getColor('white')

screen.fill(clr_back)
pygame.display.update()

position    = env.getRectPos()
updatable   = position + env.getRectSize()

avail_state = ['prev_stop', 'left', 'right', 'forward']
image_state = random.choice(avail_state)

clock       = pygame.time.Clock()
last_tick   = pygame.time.get_ticks()

image       = {}
for val in avail_state :
    image[val]      = env.getRectIMG(val)

def coverBack() :
    surface = pygame.Surface(env.getRectSize())
    surface.fill(clr_back)

    screen.blit(surface, position)

def drawRectangle(img) :
    surface = pygame.Surface(env.getRectSize())
    surface.fill(clr_default)
    surface.blit(img, (0, 0))

    screen.blit(surface, position)

def loop() :
    global counter, image_state, run

    eventLoop()
    clock.tick(fps)
    # last_tick = pygame.time.get_ticks()

    if (run) :
        if (counter == max_ctr) :
            drawRectangle(image[image_state])
            image_state = random.choice(avail_state)

            counter = 0
        else :
            coverBack()

            counter += 1

    else :
        drawRectangle(image['prev_stop'])

    pygame.display.update(updatable)

def eventLoop() :
    global run

    for event in pygame.event.get():
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE :
                pygame.quit()
                sys.exit()
            if event.key == K_SPACE :
                run = not run

def run() :
    while True :
        loop()

if __name__ == "__main__":
    run()
