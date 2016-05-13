import os, sys, time, errno, pygame, platform
import matplotlib.pyplot as plt

from emokit.emotiv import Emotiv
from datetime import datetime
from stimulus.env import Env
from pygame.locals import *

if platform.system() == "Windows":
    import socket  # Needed to prevent gevent crashing on Windows. (surfly / gevent issue #459)
import gevent

between_time   = 2
stimulus_out   = 1

try :
    name    = sys.argv[1]
except:
    name    = 'unnamed'

try :
    max_out = int(sys.argv[2])
except:
    max_out = 5

pygame.init()
info        = pygame.display.Info()
clock       = pygame.time.Clock()
env         = Env(info.current_w, info.current_h)

screen      = pygame.display.set_mode(env.getResolution(), pygame.FULLSCREEN)
clr_back    = env.getColor('black')
clr_yellow  = env.getColor('yellow')
clr_default = env.getColor('white')

screen.fill(clr_back)
pygame.display.update()

position    = env.getRectPos()
updatable   = position + env.getRectSize()

run         = True

avail_state = ['stop', 'fill_left', 'fill_right', 'fill_forward']

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

if __name__ == "__main__":
    # headset = Emotiv(display_output=False)
    headset     = Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(0)

    folder      = 'data/' + datetime.now().strftime('%Y%m%d') + '/'
    filename    = datetime.now().strftime('%H%M%S') + "_" + name + "_" + str(max_out) + ".csv"

    fullpath    = os.path.join(folder, filename)

    if not os.path.exists(os.path.dirname(fullpath)):
        try:
            os.makedirs(os.path.dirname(fullpath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    output      = open(fullpath, 'w')

    data        = {
        'second'    : [],
        'counter'   : [],
        'F3'        : [],
        'FC5'       : [],
        'AF3'       : [],
        'F7'        : [],
        'T7'        : [],
        'P7'        : [],
        'O1'        : [],
        'O2'        : [],
        'P8'        : [],
        'T8'        : [],
        'F8'        : [],
        'AF4'       : [],
        'FC6'       : [],
        'F4'        : []
    }
    # output.write("SECOND,COUNTER,F3,FC5,AF3,F7,T7,P7,O1,O2,P8,T8,F8,AF4,FC6,F4,GYRO_X,GYRO_Y\n")

    iteree      = 0
    counter     = 0
    try:
        start_time      = int(round(time.time() * 1000))
        while ( iteree < max_out ):
            time_now    = int(round(time.time() * 1000)) - start_time
            packet      = headset.dequeue()
            # output.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (time.time(), packet.counter, packet.F3[0], packet.FC5[0], packet.AF3[0], packet.F7[0], packet.T7[0], packet.P7[0], packet.O1[0], packet.O2[0], packet.P8[0], packet.T8[0], packet.F8[0], packet.AF4[0], packet.FC6[0], packet.F4[0], packet.gyro_x, packet.gyro_y))
            output.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (time_now, iteree, packet.F3[0], packet.FC5[0], packet.AF3[0], packet.F7[0], packet.T7[0], packet.P7[0], packet.O1[0], packet.O2[0], packet.P8[0], packet.T8[0], packet.F8[0], packet.AF4[0], packet.FC6[0], packet.F4[0], packet.gyro_x, packet.gyro_y))

            data['second'].append(time_now)
            data['counter'].append(iteree)
            data['F3'].append(packet.F3[0])
            data['FC5'].append(packet.FC5[0])
            data['AF3'].append(packet.AF3[0])
            data['F7'].append(packet.F7[0])
            data['T7'].append(packet.T7[0])
            data['P7'].append(packet.P7[0])
            data['O1'].append(packet.O1[0])
            data['O2'].append(packet.O2[0])
            data['P8'].append(packet.P8[0])
            data['T8'].append(packet.T8[0])
            data['F8'].append(packet.F8[0])
            data['AF4'].append(packet.AF4[0])
            data['FC6'].append(packet.FC6[0])
            data['F4'].append(packet.F4[0])

            counter += 1
            if (counter is 128) :
                counter = 0
                iteree += 1

                print iteree

            if ((iteree % between_time) is stimulus_out) :
                pass

            gevent.sleep(0)

    except KeyboardInterrupt:
        headset.close()
        os.system('clear')
        pygame.quit()
        sys.exit()

    finally:
        headset.close()
        os.system('clear')
        pygame.quit()
        sys.exit()
