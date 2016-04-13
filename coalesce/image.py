import pygame, sys, thread, time, os
from pygame.locals import *

pygame.init()
info        = pygame.display.Info()
clock       = pygame.time.Clock()

img_loc     = os.path.join("images", "arrow.png")
img         = pygame.image.load(img_loc)
img         = pygame.transform.scale(img, (400, 400))

clr_white   = (255, 255, 255)
clr_black   = (0, 0, 0)
clr_red     = (255, 0, 0)
clr_green   = (0, 255, 0)
clr_blue    = (0, 0, 255)

display     = (400, 400)
screen      = pygame.display.set_mode(display)
screen.fill(clr_blue)

def eventLoop() :
    for event in pygame.event.get():
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE :
                pygame.quit()
                sys.exit()

while True:
    eventLoop();

    screen.fill(clr_blue)
    screen.blit(img,(0,0))
    pygame.display.update()
