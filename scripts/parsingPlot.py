import os, sys, time, math, random
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
    # source      = 'data/20160503/174424_p300_stop_20.csv'
    # source      = 'data/20160503/175805_p300_forward_20.csv'
    # source      = 'data/20160503/180853_p300_left_20.csv'
    source      = 'data/20160503/181835_p300_right_20.csv'

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

def run() :
    data            = readFromFile(source)
    timestamp       = data[:,0]

    stimulus_out    = loadStimulus(5.0)
    stimulus        = findStimulus(timestamp, stimulus_out)

    stimulus_single = 0
    sampling        = (1000 / sampling_rate)
    first_cut       = stimulus[4] - stimulus_single
    second_cut      = stimulus[4] + (sampling_rate / 2)

    current         = moveToAxis(data[:,15])

    if (len(current) >= second_cut) :
        first_stimulus  = current[first_cut:second_cut]
        x               = np.arange(len(first_stimulus))

        plt.plot((x - stimulus_single) * sampling , first_stimulus)

        plt.xlabel('Time [ms]')
        plt.ylabel('Voltage')

        plt.axvline(x=0, color='r', ls='--')

        parsed      = parse(first_stimulus, split_amount)
        power       = countAllPower(parsed)
        diff        = findDifference(power)
        # print diff

        parseLine   = np.arange(0, (sampling_rate / 2), split_amount)
        for key, val in enumerate(parseLine[1:]) :
            text_axis   = (val - (split_amount / 2)) * sampling
            text_ord    = np.amax(parsed[key:key+1])

            plt.axvline(x=(val * sampling), color='g', ls='--')
            if (key < len(diff)) : plt.text(text_axis, text_ord, "{0:.2f}%".format(diff[key]))

        plt.ylim((650,820))
        plt.show()

if __name__ == "__main__":
    run()
    # print env_serial\
