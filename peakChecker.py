import sys
import time
import numpy as np
import matplotlib.pyplot as plt

from env import *
from random import randint
from datetime import datetime
from preprocess import *

low_limit       = 5
high_limit      = 20
sampling_rate   = 129

header          = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

try :
    source      = sys.argv[1]
except:
    source      = 'data/10-stop'

def readFromFile(filename) :
    with open(filename) as afile :
        result = []
        for line in afile :
            result.append(map(int, line.split(',')))

        return np.array(result)

def parse(data, count) :
    reminder    = data
    result      = []

    while len(reminder) > count:
        result.append(reminder[0:count])
        reminder    = reminder[count:]

    return result

def run() :
    start_time  = time.time()

    data        = readFromFile(source)

    # idx         = randint(2,16)
    idx         = 2

    # start       = 0
    start       = 234

    # stop        = len(data[:,0])
    stop        = 331

    single      = data[start:stop,idx]

    window      = 6
    parsed      = parse(single, window)

    windowedPower       = []
    for val in parsed   : windowedPower.append(countPower(val))

    percentageDifferent = []
    for key, val in enumerate(windowedPower) :
        if key is not 0 :
            percentageDifferent.append(countPercentageDifferent(val, windowedPower[key - 1]))

    for key, val in enumerate(percentageDifferent) :
        print str(key) + ' => ' + str((key + 2) * window)])

    plt.plot(single)
    plt.figure()
    plt.plot(percentageDifferent)
    plt.show()

    elapsed_time = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
