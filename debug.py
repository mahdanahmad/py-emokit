import os, sys, time, math, random, gevent
import numpy as np
import matplotlib.pyplot as plt

from preprocess import *

first_base      = 18
home_run        = 65

header          = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4", "Direction"]
avail_state     = ["forward", "left", "right", "stop"]
avail_channel   = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

couples         = [
    [0, 13], # F3 & F4
    [1, 12], # FC5 & FC6
    [2, 11], # AF3 & AF4
    [3, 10], # F7 & F8
    [4, 9],  # T7 & T8
    [5, 8],  # P7 & P8
    [6, 7]   # O1 & O2
]

directories = ['data/20160530']

def readFromFile(filename) :
    with open(filename) as afile :
        result = []
        for line in afile :
            # print line.split(',')
            splittedLine    = line.split(',')
            result.append([float(splittedLine[0])] +  map(int, splittedLine[1::1]))

        return np.array(result)

def loadStimuli(source) :
    stimuliPath = 'result/stimulus' + source.replace('data', '')
    with open(stimuliPath) as afile :
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

    sum_channel     = {}
    for state in avail_state :
        sum_channel[state]  = {}
        for channel in avail_channel :
            sum_channel[state][channel] = 0

    for current_dir in directories :
        for file in os.listdir(current_dir):
            source      = current_dir + '/' + file
            print source

            data        = readFromFile(source)
            timestamp   = data[:,0]

            stimuli     = loadStimuli(source)
            stimuli_pos = findStimulus(timestamp, stimuli['time'])

            for stimulus_idx, stimulus_pos in enumerate(stimuli_pos) :
                iteree      = range(2, 16)
                direction   = stimuli['direction'][stimulus_idx]

                if ((stimulus_pos + home_run) <= len(data[:,0])) :
                    channel_vals    = []
                    for key, val in enumerate(iteree) :
                        current         = moveToAxis(data[:,val][stimulus_pos:(stimulus_pos + home_run)])
                        suspectedMax    = max(current[first_base:])
                        averageBefore   = np.average(current[:first_base])

                        max_peak        = suspectedMax - averageBefore
                        channel_vals.append(int(math.ceil(max_peak)))

                    for val in couples :
                        left_side   = val[0]
                        right_side  = val[1]
                        difference  = channel_vals[left_side] - channel_vals[right_side]

                        if difference > 0 :
                            sum_channel[direction][avail_channel[val[0]]]   += 1
                        else :
                            sum_channel[direction][avail_channel[val[1]]]   += 1


        fullpath        = os.path.join('result/dump_channel.csv')
        if not os.path.exists(os.path.dirname(fullpath)):
            try:
                os.makedirs(os.path.dirname(fullpath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        output          = open(fullpath, 'w')
        output.write(','.join(header) + '\n')


    elapsed_time    = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
