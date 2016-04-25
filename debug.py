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

def loadStimulus(diff=0)  :
    with open('data/stimulus_out.csv') as afile :
        result  = []
        for line in afile :
            result.append(float(line) + diff)

        return np.array(result)

def run() :
    start_time      = time.time()
    data            = readFromFile(source)
    timestamp       = data[:,0]

    stimulus_out    = loadStimulus(4.0)
    stimulus        = findStimulus(timestamp, stimulus_out, 6)

    single          = data[:,13]
    normalize       = normalization(single)
    moved           = moveToAxis(single)
    filtered        = doFiltering(normalize, 0, 8, 129)
    parsed          = parse(moved, 6)
    power           = countAllPower(parsed)
    diff            = findDifference(power)

    plt.plot(single)
    plt.title('Normal Signal')
    plt.figure()
    plt.plot(normalize)
    # plt.title('Normalized Signal')
    for val in range(1, 10) : plt.axvline(x=val * 6, color='0.5', ls='--')
    plt.figure()
    plt.plot(diff)
    for val in stimulus : plt.axvline(x=val, color='r', ls='--')
    plt.title('Power Difference')
    plt.show()

    elapsed_time    = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
