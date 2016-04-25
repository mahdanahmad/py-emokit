import sys
import time
import numpy as np
import matplotlib.pyplot as plt

from env import *
from datetime import datetime
from preprocess import *

low_limit       = 5
high_limit      = 20
split_amount    = 6
sampling_rate   = 129

header          = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

try :
    source      = sys.argv[1]
except:
    source      = 'data/10-stop'

try :
    balancer    = float(sys.argv[2])
except:
    balancer    = 0

def readFromFile(filename) :
    with open(filename) as afile :
        result = []
        for line in afile :
            splittedLine    = line.split(',')
            result.append([float(splittedLine[0])] +  map(int, splittedLine[1::1]))

        return np.array(result)

def loadStimulus(difference=0)  :
    with open('data/stimulus_out.csv') as afile :
        result  = []
        for line in afile :
            result.append(float(line) + difference)

        return np.array(result)

def run() :
    data            = readFromFile(source)
    timestamp       = data[:,0]
    stimulus_out    = loadStimulus(balancer)

    stimulus        = findStimulus(timestamp, stimulus_out, split_amount)

    channel         = []
    unprocessed     = []
    for i in range(2, 16)   :
        current     = moveToAxis(data[:,i])
        filtered    = doFiltering(current, 0, 8, 129)
        parsed      = parse(current, split_amount)
        power       = countAllPower(parsed)
        diff        = findDifference(power)

        channel.append(diff)
        unprocessed.append(current)

        plt.plot(diff)
        plt.title(header[i-2])
        for val in stimulus : plt.axvline(x=val, color='r', ls='--')
        if (i < 15) : plt.figure()

    # selected        = 2
    #
    # plt.plot(unprocessed[selected])
    # for val in findStimulus(timestamp, stimulus_out) : plt.axvline(x=val, color='r', ls='--')
    # plt.figure()
    # plt.plot(channel[selected])
    # for val in stimulus : plt.axvline(x=val, color='r', ls='--')

    plt.show()

if __name__ == "__main__":
    run()
