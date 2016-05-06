import os
import sys
import time
import math
import random
import numpy as np
import matplotlib.pyplot as plt

from env import *
from datetime import datetime
from preprocess import *

low_limit       = 5
high_limit      = 20
sampling_rate   = 129
split_amount    = 6

header          = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

try :
    source      = sys.argv[1]
except:
    # source      = 'data/10-stop'
    source      = 'data/20160503/174424_p300_stop_20.csv'

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
            result.append(float(line) - diff)

        return np.array(result)

def countDiff(data) :
    result          = parse(data, 6)
    result          = countAllPower(result)
    result          = findDifference(result)

    return result

def run() :
    start_time      = time.time()

    data            = readFromFile(source)
    timestamp       = data[:,0]

    stimulus_out    = loadStimulus(5.0)
    stimulus        = findStimulus(timestamp, stimulus_out)

    stimulus_single = (int)(sampling_rate / 3)
    first_cut       = stimulus[3] - stimulus_single
    second_cut      = stimulus[3] + sampling_rate
    sampling        = (1000 / sampling_rate)
    for i in range(2, 16) :
        current         = moveToAxis(data[:,i])
        first_stimulus  = current[first_cut:second_cut]
        x               = np.arange(len(first_stimulus))

        plt.plot(x * sampling , first_stimulus)

        plt.axvline(x=(stimulus_single * sampling), color='r', ls='--')
        plt.axvline(x=((stimulus_single * sampling) + 140), color='g', ls='--')
        plt.axvline(x=((stimulus_single * sampling) + 500), color='g', ls='--')

        first_base      = (int)(stimulus_single + math.floor(sampling_rate * 0.14))
        end_game        = (int)(stimulus_single + math.ceil(sampling_rate * 0.50))

        suspectedPower  = countPower(first_stimulus[first_base:end_game])
        totalPower      = countPower(first_stimulus[stimulus_single:end_game])

        percentage      = (suspectedPower * 100) / totalPower
        # print percentage

        plt.title("{0:.2f}%".format(percentage))

        if (i < 15) : plt.figure()

    plt.show()

    elapsed_time    = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
