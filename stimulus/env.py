from pygame.locals import *
import pygame, os

 #
 # Editable Configuration
 #

fps             = {
    'global'    : 60,
    'forward'   : 9,
    'stop'      : 10,
    'right'     : 11,
    'left'      : 12
}

images_folder   = 'images'
filename        = {
    'stop'      : 'circle-stop.png',
    'left'      : 'arrow-left.png',
    'right'     : 'arrow-right.png',
    'forward'   : 'arrow-forward.png'
}

side_divider    = 4
grid            = 4         # column and row
position        = {         # based on grid
    'stop'      : (2, 3),
    'left'      : (1, 3),
    'right'     : (3, 3),
    'forward'   : (2, 1)
}

 #
 # Environment Class
 # @param int screenWidth
 # @param int screenHeight
 #

class Env():
    def __init__(self, screenWidth, screenHeight, name='Stimulus Environment') :
        self.__clr_white    = (255, 255, 255)
        self.__clr_black    = (0, 0, 0)
        self.__clr_red      = (255, 0, 0)
        self.__clr_green    = (0, 255, 0)
        self.__clr_blue     = (0, 0, 255)

        self.__width        = screenWidth
        self.__height       = screenHeight
        self.__resolution   = (self.__width, self.__height)

        self.__side         = self.__height / side_divider

        self.__run          = True
        self.__stop         = False

        self.__fps          = fps['global']
        self.__fps_forward  = fps['forward']
        self.__fps_stop     = fps['stop']
        self.__fps_right    = fps['right']
        self.__fps_left     = fps['left']

        self.__img_stop     = self.__setImage('stop')
        self.__img_left     = self.__setImage('left')
        self.__img_right    = self.__setImage('right')
        self.__img_forward  = self.__setImage('forward')

        self.__pos_stop     = self.__setRectPosition(grid, position['stop'])
        self.__pos_left     = self.__setRectPosition(grid, position['left'])
        self.__pos_right    = self.__setRectPosition(grid, position['right'])
        self.__pos_forward  = self.__setRectPosition(grid, position['forward'])

    def killStop(self)      : self.__stop = True
    def changeRun(self)     : self.__run  = not self.__run

    def getRun(self)                : return self.__run
    def getStop(self)               : return self.__stop
    def getResolution(self)         : return self.__resolution
    def getRectSize(self)           : return (self.__side, self.__side)

    def getIMG(self, state=None)        :
        return {
            'stop'          : self.__img_stop,
            'left'          : self.__img_left,
            'right'         : self.__img_right,
            'forward'       : self.__img_forward
        }.get(state, self.__img_stop)

    def getFPS(self, state=None)        :
        return {
            'global'        :self.__fps,
            'left'          :self.__fps_left,
            'stop'          :self.__fps_stop,
            'right'         :self.__fps_right,
            'forward'       :self.__fps_forward
        }.get(state, self.__fps)

    def getColor(self, state=None)      :
        return {
            'white'         : self.__clr_white,
            'black'         : self.__clr_black,
            'red'           : self.__clr_red,
            'green'         : self.__clr_green,
            'blue'          : self.__clr_blue
        }.get(state, self.__clr_white)

    def getRectPos(self, state=None)    :
        return {
            'stop'          : self.__pos_stop,
            'left'          : self.__pos_left,
            'right'         : self.__pos_right,
            'forward'       : self.__pos_forward
        }.get(state, self.__pos_stop)

    def __setImage(self, state) :
        fullpath            = os.path.join(images_folder, filename[state])
        raw_img             = pygame.image.load(fullpath)

        return pygame.transform.scale(raw_img, (self.__side, self.__side))

    def __setRectPosition(self, grid, pos) :
        X   = (self.__width / grid) * pos[0] - (self.__side / 2)
        Y   = (self.__height / grid) * pos[1] - (self.__side / 2)

        return (X, Y)
