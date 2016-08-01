import os, sys, time, math, random, gevent
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import *

first_base  = 18
home_run    = 65

header      = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

source      = "data/20160513/185916_Arif_5.csv"
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

    print source

    data        = readFromFile(source)
    timestamp   = data[:,0]

    stimuli     = loadStimuli(source)
    stimuli_pos = findStimulus(timestamp, stimuli['time'])

    stimulus_idx    = random.randrange(0, len(stimuli_pos))
    stimulus_pos    = stimuli_pos[stimulus_idx]

    direction   = stimuli['direction'][stimulus_idx]

    iteree      = range(2, 16)
    if ((stimulus_pos + home_run) <= len(data[:,0])) :
        for key, val in enumerate(iteree) :
            current         = moveToAxis(data[:,val][stimulus_pos:(stimulus_pos + home_run)])
            suspectedMax    = max(current[first_base:home_run])
            averageBefore   = np.average(current[:first_base])
            percentageDiff  = countPercentageDifferent(suspectedMax, averageBefore)

            # suspectedPower  = countPower(current[first_base:home_run])
            # totalPower      = countPower(current[:home_run])
            # percentageDiff  = (suspectedPower * 100) / totalPower

            yPlot           = moveToAxis(data[:,val][(stimulus_pos):(stimulus_pos + 65)])
            xPlot           = timestamp[(stimulus_pos):(stimulus_pos + 65)] - timestamp[stimulus_pos]

            # plt.axvline(x=0, color='r', ls='--')
            # plt.axvline(x=(timestamp[stimulus_pos + 14] - timestamp[stimulus_pos]), color='r', ls='--')
            # plt.axvline(x=(timestamp[stimulus_pos + first_base] - timestamp[stimulus_pos]), color='g', ls='--')
            # plt.axvline(x=(timestamp[stimulus_pos + home_run] - timestamp[stimulus_pos]), color='g', ls='--')
            plt.axvline(x=140, color='g', ls='--')
            plt.axvline(x=465, color='g', ls='--')

            plt.plot(xPlot, yPlot)
            plt.title("{0:.2f}%".format(percentageDiff))

            plt.xlabel('time [Hz]')
            plt.ylabel(u'Voltage [\u00B5V]')

            plotFile        = plotRoot + '/' + header[val - 2] + '.jpg'
            # print plotFile

            print header[val - 2] + ' = ' +  str(suspectedMax) + ' | ' + str(averageBefore) + ' | ' + str(percentageDiff)

            if not os.path.exists(os.path.dirname(plotFile)):
                try:
                    os.makedirs(os.path.dirname(plotFile))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            plt.savefig(plotFile)
            plt.clf()

            # if (key < (len(iteree) - 1)) :
                # plt.figure()
            # else :
                # plt.show()

    elapsed_time    = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
