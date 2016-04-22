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
            # print line.split(',')
            splittedLine    = line.split(',')
            result.append([float(splittedLine[0])] +  map(int, splittedLine[1::1]))

        return np.array(result)

def loadStimulus()  :
    with open('data/stimulus_out.csv') as afile :
        result  = []
        for line in afile :
            result.append(float(line))

        return np.array(result)

def run() :
    start_time      = time.time()
    stimulus_out    = loadStimulus()

    data            = readFromFile(source)

    single          = moveToAxis(data[:,6])
    # single          = (data[:,6])
    timestamp       = data[:,0]
    filtered        = doFiltering(single, 0, 8, 129)

    height          = single.max()
    x               = np.arange(len(single))
    timeline        = []
    for val in timestamp:
        if (val in stimulus_out) :
            print val
            timeline.append(height)
        else :
            timeline.append(0)

    plt.plot(x, single, 'b', x, timeline, 'r--')
    plt.show()

    elapsed_time = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
