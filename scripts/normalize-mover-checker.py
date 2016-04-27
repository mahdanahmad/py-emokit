import os, sys, time
import numpy as np
import matplotlib.pyplot as plt

from random import randint
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

    data            = readFromFile(source)
    timestamp       = data[:,0]

    stimulus_out    = loadStimulus(4.0)
    stimulus        = findStimulus(timestamp, stimulus_out, 6)

    single          = data[:,3]
    moved           = moveToAxis(single)
    normalize       = normalization(single)
    filtered_single = doFiltering(single, 0, 8, 129)
    filtered_moved  = doFiltering(moved, 0, 8, 129)

    # print 'filtered_single'
    # print filtered_single
    # print 'filtered_moved'
    # print filtered_moved

    diff_single             = countDiff(single)
    diff_moved              = countDiff(moved)
    diff_normalize          = countDiff(normalize)
    diff_filtered_single    = countDiff(filtered_single)
    diff_filtered_moved     = countDiff(filtered_moved)

    # print 'diff_filtered_single'
    # print diff_filtered_single
    # print 'diff_filtered_moved'
    # print diff_filtered_moved

    plt.plot(single)
    plt.title('Normal Signal')
    plt.figure()
    plt.plot(moved)
    plt.title('Moved Signal')
    plt.figure()
    plt.plot(normalize)
    plt.title('Normalized Signal')
    plt.figure()
    plt.plot(filtered_single)
    plt.title('Filtered Single')
    plt.figure()
    plt.plot(filtered_moved)
    plt.title('Filtered Moved')
    plt.figure()
    plt.plot(diff_single)
    plt.title('Percentage Difference Normal Signal')
    plt.figure()
    plt.plot(diff_moved)
    plt.title('Percentage Difference Moved Signal')
    plt.figure()
    plt.plot(diff_normalize)
    plt.title('Percentage Difference Normalized Signal')
    plt.figure()
    plt.plot(diff_filtered_single)
    plt.title('Percentage Difference Filtered Single')
    plt.figure()
    plt.plot(diff_filtered_moved)
    plt.title('Percentage Difference Filtered Moved')
    plt.show()
    # for val in stimulus : plt.axvline(x=val, color='r', ls='--')
    # for val in range(1, 10) : plt.axvline(x=val * 6, color='0.5', ls='--')

    elapsed_time    = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
