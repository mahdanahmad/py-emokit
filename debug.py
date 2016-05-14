import os
import sys
import time
import math
import random
import gevent
import numpy as np
import matplotlib.pyplot as plt

from env import *
from datetime import datetime
from preprocess import *

low_limit       = 5
high_limit      = 20
sampling_rate   = 128
split_amount    = 6

header          = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

try :
    source      = sys.argv[1]
except:
    source      = 'data/20160513/184727_Arif_5.csv'

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

def loadNewStimulus(source) :
    stimulusPath    = 'result/stimulus' + source.replace('data', '')
    with open(stimulusPath) as afile :
        result  = {
            'time'      : [],
            'direction' : []
        }
        for line in afile :
            splittedLine    = line.rstrip().split(',')
            result['time'].append(int(splittedLine[0]))
            result['direction'].append(splittedLine[1])

        return result

def run() :
    start_time      = time.time()

    data            = readFromFile(source)
    timestamp       = data[:,0]
    stimulus_list   = loadNewStimulus(source)
    stimulus_pos    = findStimulus(timestamp, stimulus_list['time'])

    first_cut       = stimulus_pos[0] - 15
    second_cut      = stimulus_pos[0] + sampling_rate

    iteree          = range(2, 16)
    for idx, i in enumerate(iteree) :
        current     = moveToAxis(data[:,i][first_cut:second_cut])
        x           = timestamp[first_cut:second_cut] - timestamp[stimulus_pos[0]]

        plt.plot(x, current)

        plt.xlabel('Time [ms]')
        plt.ylabel('Voltage')

        plt.axvline(x=0, color='r', ls='--')
        plt.axvline(x=140, color='g', ls='--')
        plt.axvline(x=500, color='g', ls='--')

        if (idx < (len(iteree) - 1)) :
            plt.figure()
        else :
            plt.show()

    elapsed_time    = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
