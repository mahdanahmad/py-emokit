import sys
import time
import numpy as np
import matplotlib.pyplot as plt

from env import *
from datetime import datetime
from preprocess import *

low_limit       = 5
high_limit      = 20
split_amount    = 5
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

def parse(data) :
    reminder    = data
    result      = []

    while len(reminder) > sampling_rate:
        result.append(reminder[0:sampling_rate])
        reminder    = reminder[sampling_rate:]

    return result

def preprocess(data) :
    result      = data
    result[:]   = [doCentering(val) for val in result]
    result[:]   = [doFiltering(val, low_limit, high_limit, sampling_rate, 10) for val in result]
    result[:]   = [createFFT(val) for val in result]
    result[:]   = [createPSD(val, sampling_rate) for val in result]

    return result

def plotAll(data) :
    for key, val in enumerate(data):
        if (key < len(data) - 1) :
            plt.plot(val)
            plt.title('data detik ke-' + str(key + 1))
            if (key < len(data) - 2) : plt.figure()

    plt.show()

def findPeak(data) :
    # result  = {}
    result  = []
    for key, val in enumerate(data):
        # result[key] = np.argmax(val)
        result.append(np.argmax(val))

    return result

def run() :
    data        = readFromFile(source)

    occipital   = []
    for i in range(8, 10)   : occipital.append(data[:,i])

    indices = {
        'O1'    : {},
        'O2'    : {}
    }

    for i in range(0, 129) :
        for key, val in enumerate(occipital):
            current     = parse(val[i:])
            PSD_result  = preprocess(current)
            peak_array  = findPeak(PSD_result)

            if 10 in peak_array :
                peak_pos    = peak_array.index(10)

                if peak_pos in indices["O" + str(key + 1)].keys() :
                    indices["O" + str(key + 1)][peak_pos]  += 1
                else :
                    indices["O" + str(key + 1)][peak_pos]   = 1
                print "O" + str(key + 1) + " detik ke- " + str(peak_pos) + " => " + str(peak_array)

    print indices

if __name__ == "__main__":
    run()
    # print env_serial\
