from pygame.locals import *
import pygame, threading, os, sys

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

forwardX    = (width / 4) * 2 - (def_side / 2)
forwardY    = (height / 4) * 1 - (def_side / 2)
forwardFPS  = 9
forwardIMG  = pygame.transform.scale(pygame.image.load(os.path.join("images", "arrow-forward.png")), (def_side, def_side))

stopX       = (width / 4) * 2 - (def_side / 2)
stopY       = (height / 4) * 3 - (def_side / 2)
stopFPS     = 10
stopIMG     = pygame.transform.scale(pygame.image.load(os.path.join("images", "circle-stop.png")), (def_side, def_side))

rightX      = (width / 4) * 3 - (def_side / 2)
rightY      = (height / 4) * 3 - (def_side / 2)
rightFPS    = 11
rightIMG    = pygame.transform.scale(pygame.image.load(os.path.join("images", "arrow-right.png")), (def_side, def_side))

leftX       = (width / 4) * 1 - (def_side / 2)
leftY       = (height / 4) * 3 - (def_side / 2)
leftFPS     = 12
leftIMG     = pygame.transform.scale(pygame.image.load(os.path.join("images", "arrow-left.png")), (def_side, def_side))

global_fps  = 60
global_run  = True
global_stop = False
global_lock = threading.Lock()

screen.fill(clr_back)

class Rectangle(threading.Thread):
    def __init__(self, name='Unnamed', freq=10, posX=0, posY=0, img=None) :
        threading.Thread.__init__(self)
        self.clock      = pygame.time.Clock()
        self.surface    = pygame.Surface((def_side, def_side))
        self.up         = 0
        self.name       = name
        self.image      = img
        self.delay      = 1000 / (freq * 2)

        self.pos        = (posX, posY)
        self.rect       = (posX, posY, def_side, def_side)

        # print self.delay
        # self.count      = 0
        # self.init_tick  = pygame.time.get_ticks()
    def run(self) :
        while True :
            if global_stop :
                return
            else :
                self.loop()

    def loop(self) :
        self.clock.tick()

        if (global_run) :
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
    global global_run
    global global_stop

    for event in pygame.event.get():
        if event.type == QUIT :
            global_stop = True

            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN :
            if event.key == K_ESCAPE :
                global_stop = True

                pygame.quit()
                sys.exit()
            if event.key == K_SPACE :
                global_run = not global_run

def run() :
    forward = Rectangle('forward', forwardFPS, forwardX, forwardY, forwardIMG)
    forward.start()

    stop    = Rectangle('stop', stopFPS, stopX, stopY, stopIMG)
    stop.start()

    right   = Rectangle('right', rightFPS, rightX, rightY, rightIMG)
    right.start()

    left    = Rectangle('left', leftFPS, leftX, leftY, leftIMG)
    left.start()

    while True :
        eventLoop()
        clock.tick(global_fps)

if __name__ == "__main__":
    run()
