import pygame, sys
from pygame.locals import *
import random

FPS = 30  # frames per second
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Thing(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super(Thing, self).__init__(*args, **kwargs)  # init Rect base class
        # define additional attributes
        self.color = tuple(random.randrange(0, 256) for _ in range(3))
        self.x_speed, self.y_speed = 5, 5  # how fast it moves

    def draw(self, surface, width=0):
        pygame.draw.rect(surface, self.color, self, width)

def main():
    pygame.init()
    fpsclock = pygame.time.Clock()
    pygame.key.set_repeat(250)  # enable keyboard repeat for held down keys
    gameDisplay = pygame.display.set_mode((500,400), 0,32)
    gameDisplay.fill(WHITE)

    thingx,thingy, thingw,thingh = 200,150, 100,50
    thing = Thing(thingx, thingy, thingw, thingh)  # create an instance

    while True:  # display update loop
        gameDisplay.fill(WHITE)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    thing.y += thing.y_speed
                elif event.key == K_UP:
                    thing.y -= thing.y_speed
                elif event.key == K_RIGHT:
                    thing.x += thing.x_speed
                elif event.key == K_LEFT:
                    thing.x -= thing.x_speed

        thing.draw(gameDisplay)  # display at current position
        pygame.display.update()
        fpsclock.tick(FPS)

main()
