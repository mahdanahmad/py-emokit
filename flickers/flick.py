import pygame, sys, thread, time
from pygame.locals import *

pygame.init()
info        = pygame.display.Info()
clock       = pygame.time.Clock()

width       = info.current_w
height      = info.current_h

display     = (width, height)
screen      = pygame.display.set_mode(display, pygame.FULLSCREEN)

# run         = False

clr_white   = (255, 255, 255)
clr_black   = (0, 0, 0)
clr_red     = (255, 0, 0)
clr_green   = (0, 255, 0)
clr_blue    = (0, 0, 255)

clr_default = clr_white

# def_width   = 800
# def_height  = 600
def_side    = 200

fps_forward = 12
fps_stay    = 15

screen.fill(clr_black)

class Rectangle(pygame.Rect):
    def __init__(self, posX, posY, fps) :
        self.clock      = pygame.time.Clock()
        self.last_tick  = pygame.time.get_ticks()

        self.run    = False

        self.fps    = fps
        self.posX   = posX
        self.posY   = posY

        self.rect   = pygame.Surface((def_side, def_side))
        self.rect.fill(clr_default)

        self.alpha  = 0

        # while True :
        #     self.loop()

    def loop(self) :
        self.eventLoop()

        self.last_tick = pygame.time.get_ticks()
        self.clock.tick(self.fps)

        screen.fill(clr_black)
        if (self.run) :
            if self.alpha == 0 :
                self.alpha  = 255
            elif self.alpha == 255 :
                self.alpha  = 0
        else :
            self.alpha = 255

        self.rect.set_alpha(self.alpha)
        screen.blit(self.rect, (self.posX, self.posY))

        pygame.display.update()

        # print self.alpha

    def eventLoop(self) :
        for event in pygame.event.get():
            if event.type == KEYDOWN :
                if event.key == K_SPACE :
                    self.run = not self.run

    # def draw(self) :
    #     screen.blit(pygame.draw.rect(clr_default, (def_side, def_side)))
    #     pygame.draw.rect(screen, clr_default, self, width)
    # def refresh(self, fps) :
    #     global run
    #     if run :
    #         self.show   = not self.show
    #         if self.show :
    #             self.draw()
    #         # else :
    #             # screen.fill(clr_black)
    #
    #         pygame.display.update()
    #         clock.tick(fps)
    #     else :
    #         self.draw()

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

def loop(forward, stay) :
    eventLoop()

    forward.loop()
    stay.loop()
    # for event in pygame.event.get():
    #     if event.type == KEYDOWN :
    #         if event.key == K_SPACE :
    #             forward.refresh()
    #             pygame.display.update()
    # forward.refresh()


    # clock.tick(12)
    # global run
    # if run :
        # forward.refresh()
        # pygame.display.update()

def run() :
    forward = Rectangle((width / 2) - (def_side / 2), (height / 4 * 1) - (def_side / 2), fps_forward)
    thread.start_new_thread(forward.loop, ())
    stay    = Rectangle((width / 2) - (def_side / 2), (height / 4 * 3) - (def_side / 2), fps_stay)
    thread.start_new_thread(stay.loop, ())

    while True:  # display update loop
        eventLoop()
        pass
        # loop(forward, stay)

    # pygame.display.flip()

if __name__ == "__main__":
    run()
