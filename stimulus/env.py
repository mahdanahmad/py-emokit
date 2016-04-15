from pygame.locals import *
import pygame, os, sys

side_divider    = 4
images_folder   = 'images'
filename        = {
    'stop'      : 'circle-stop.png',
    'left'      : 'arrow-left.png',
    'right'     : 'arrow-right.png',
    'forward'   : 'arrow-forward.png'
}


class Env():
    def __init__(self, pygameInfo, name='Stimulus Environment') :
        self.width          = info.current_w
        self.height         = info.current_h
        self.display        = (width, height)

        self.side           = height / side_divider

        self.run            = True
        self.stop           = False

        self.clr_white      = (255, 255, 255)
        self.clr_black      = (0, 0, 0)
        self.clr_red        = (255, 0, 0)
        self.clr_green      = (0, 255, 0)
        self.clr_blue       = (0, 0, 255)

        self.fps            = 60
        self.fps_forward    = 9
        self.fps_stop       = 10
        self.fps_right      = 11
        self.fps_left       = 12

        # self.img_stop       = self.setImage

    def setImage(self, state) :
        fullpath            = os.path.join(images_folder, filename[state])
        raw_img             = pygame.image.load(fullpath)

        return pygame.transform.scale(raw_img, (self.side, self.side))

    def setPosition() :


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
