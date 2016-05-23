import os, sys, time, math, random, gevent
import numpy as np
import matplotlib.pyplot as plt

from preprocess import *

first_base  = 18
home_run    = 192

header      = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

directory   = ['data/20160513']
plotIteree  = {}
plotRoot    = 'result/dump/'

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

    min_peak        = []
    max_peak        = []

    for current_dir in directory :
        for afile in os.listdir(current_dir):
            source      = current_dir + '/' + afile
            print source

            data        = readFromFile(source)
            timestamp   = data[:,0]

            stimuli     = loadStimuli(source)
            stimuli_pos = findStimulus(timestamp, stimuli['time'])

            plotGuinea  = source.split('_')[1]
            plotDir     = plotRoot + plotGuinea + '/'

            if plotGuinea not in plotIteree : plotIteree[plotGuinea] = { 'left' : 1, 'right' : 1, 'forward' : 1, 'stop' : 1 }

            for stimulus_idx, stimulus_pos in enumerate(stimuli_pos) :
                direction   = stimuli['direction'][stimulus_idx]
                currIteree  = plotIteree[plotGuinea][direction]
                plotIteree[plotGuinea][direction]   += 1

                plotPath    = plotDir + direction + '/' + str(currIteree)

                iteree      = range(2, 16)
                if ((stimulus_pos + home_run) <= len(data[:,0])) :
                    for key, val in enumerate(iteree) :
                        current         = moveToAxis(data[:,val][stimulus_pos:(stimulus_pos + home_run)])

                        min_peak.append(np.argmin(current))
                        max_peak.append(np.argmax(current))

                        # print "min : " + str(np.argmin(current)) + ". max : " + str(np.argmax(current))

    print "max : " + str(np.amin(max_peak)) + " - " + str(np.amax(max_peak)) + ". mean : " + str(np.mean(max_peak)) + ". most : " + str(np.bincount(max_peak).argmax())
    print "min : " + str(np.amin(min_peak)) + " - " + str(np.amax(min_peak)) + ". mean : " + str(np.mean(min_peak)) + ". most : " + str(np.bincount(min_peak).argmax())

    plt.bar(np.arange(len(np.bincount(max_peak))), np.bincount(max_peak), align='center', alpha=0.5)
    plt.figure()
    plt.bar(np.arange(len(np.bincount(min_peak))), np.bincount(min_peak), align='center', alpha=0.5)
    plt.show()

    elapsed_time    = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
