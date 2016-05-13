from emokit.emotiv import Emotiv
from datetime import datetime
from preprocess import *

import os, sys, time, errno, platform
import matplotlib.pyplot as plt

if platform.system() == "Windows":
    import socket  # Needed to prevent gevent crashing on Windows. (surfly / gevent issue #459)
import gevent

try :
    name    = sys.argv[1]
except:
    name    = 'unnamed'
    
try :
    maxtime = int(sys.argv[2])
except:
    maxtime = 10

if __name__ == "__main__":
    # headset = Emotiv(display_output=False)
    headset     = Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(0)

    folder      = 'data/' + datetime.now().strftime('%Y%m%d') + '/'
    filename    = datetime.now().strftime('%H%M%S') + "_" + name + "_" + str(maxtime) + ".csv"

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

    second      = 0
    first       = -1
    try:
        start_time      = int(round(time.time() * 1000))
        while ( second < maxtime ):
            time_now    = start_time - int(round(time.time() * 1000))
            packet      = headset.dequeue()
            # output.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (time.time(), packet.counter, packet.F3[0], packet.FC5[0], packet.AF3[0], packet.F7[0], packet.T7[0], packet.P7[0], packet.O1[0], packet.O2[0], packet.P8[0], packet.T8[0], packet.F8[0], packet.AF4[0], packet.FC6[0], packet.F4[0], packet.gyro_x, packet.gyro_y))
            output.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (time_now, packet.counter, packet.F3[0], packet.FC5[0], packet.AF3[0], packet.F7[0], packet.T7[0], packet.P7[0], packet.O1[0], packet.O2[0], packet.P8[0], packet.T8[0], packet.F8[0], packet.AF4[0], packet.FC6[0], packet.F4[0], packet.gyro_x, packet.gyro_y))

            data['second'].append(time_now)
            data['counter'].append(packet.counter)
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

            if (first == -1) :
                first = packet.counter
            else :
                if (packet.counter == (first - 1)) :
                    second  = second + 1
                    print second

            gevent.sleep(0)

    except KeyboardInterrupt:
        headset.close()
        os.system('clear')
    finally:
        headset.close()
        os.system('clear')
