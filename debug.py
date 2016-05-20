import os, sys, time, math, random, gevent
import numpy as np
import matplotlib.pyplot as plt

from preprocess import *

first_base  = 18
home_run    = 65

plot_number = 14

source      = 'data/20160513/184727_Arif_5.csv'
header      = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

plotIteree  = {}

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

    data        = readFromFile(source)
    timestamp   = data[:,0]

    stimuli     = loadStimuli(source)
    stimuli_pos = findStimulus(timestamp, stimuli['time'])

    guineaName  = source.split('_')[1]

    for stimulus_idx, stimulus_pos in enumerate(stimuli_pos[:1]) :
        iteree      = range(2, 16)

        if ((stimulus_pos + home_run) <= len(data[:,0])) :
            for key, val in enumerate(iteree) :
                current         = moveToAxis(data[:,val][stimulus_pos:(stimulus_pos + home_run)])
                suspectedMax    = max(current[first_base:home_run])
                averageBefore   = np.average(current[first_base:home_run])
                percentageDiff  = countPercentageDifferent(suspectedMax, averageBefore)

                yPlot           = moveToAxis(data[:,val][(stimulus_pos - 15):(stimulus_pos + 192)])
                xPlot           = timestamp[(stimulus_pos - 15):(stimulus_pos + 192)] - timestamp[stimulus_pos]

                plt.axvline(x=0, color='r', ls='--')
                plt.axvline(x=(timestamp[stimulus_pos + 14] - timestamp[stimulus_pos]), color='r', ls='--')
                plt.axvline(x=(timestamp[stimulus_pos + first_base] - timestamp[stimulus_pos]), color='g', ls='--')
                plt.axvline(x=(timestamp[stimulus_pos + home_run] - timestamp[stimulus_pos]), color='g', ls='--')

                plt.plot(xPlot, yPlot)
                plt.title("{0:.2f}%".format(percentageDiff))
                if (key < (len(iteree) - 1)) :
                    plt.figure()
                else :
                    # plt.show()

    elapsed_time    = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
