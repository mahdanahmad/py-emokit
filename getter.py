from emokit.emotiv import Emotiv
from datetime import datetime
from preprocess import *

import os, sys, platform
import matplotlib.pyplot as plt

if platform.system() == "Windows":
    import socket  # Needed to prevent gevent crashing on Windows. (surfly / gevent issue #459)
import gevent

if __name__ == "__main__":
    try :
        name    = sys.argv[1]
    except:
        name    = 'unnamed'
    try :
        time    = int(sys.argv[2])
    except:
        time    = 10

    # headset = Emotiv(display_output=False)
    headset     = Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(0)

    folder      = 'data/fresh/'
    filename    = datetime.now().strftime('%Y%m%d-%H%M%S') + "_" + name + "_" + str(time) + ".csv"

    fullpath    = os.path.join(folder, filename)
    output      = open(fullpath, 'w')

    O1          = []
    O2          = []
    # output.write("SECOND,COUNTER,F3,FC5,AF3,F7,T7,P7,O1,O2,P8,T8,F8,AF4,FC6,F4,GYRO_X,GYRO_Y\n")

    second      = 0
    first       = -1
    try:
        while ( second < time ):
            packet = headset.dequeue()
            output.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (second, packet.counter, packet.F3[0], packet.FC5[0], packet.AF3[0], packet.F7[0], packet.T7[0], packet.P7[0], packet.O1[0], packet.O2[0], packet.P8[0], packet.T8[0], packet.F8[0], packet.AF4[0], packet.FC6[0], packet.F4[0], packet.gyro_x, packet.gyro_y))

            O2.append(packet.O1[0])
            O2.append(packet.O2[0])

            if (first == -1) :
                first = packet.counter
            else :
                if (packet.counter == first) :
                    second  = second + 1
                    print second

            gevent.sleep(0)

    except KeyboardInterrupt:
        headset.close()
        os.system('clear')
    finally:
        headset.close()
        os.system('clear')
        # print O2
        # print filename

        data        = []
        data.append(O1)
        data.append(O2)

        data[:] = [doCentering(val) for val in data]
        data[:] = [doFiltering(val, 4, 30, 129, 10) for val in data]
        data[:] = [createFFT(val) for val in data]
        data[:] = [createPSD(val, 129) for val in data]

        for key, val in enumerate(data):
            plt.plot(val)
            if (key < (len(data) - 1)) :
                plt.figure()

        plt.show()
