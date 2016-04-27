import os
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
split_amount    = 6

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

def countDiff(data) :
    result          = parse(data, 6)
    result          = countAllPower(result)
    result          = findDifference(result)

    return result

def run() :
    start_time      = time.time()

    elapsed_time    = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
