import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import *

first_base  = 18
home_run    = 65

header          = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4","Direction"]

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
    fullpath        = os.path.join('result', 'dump_p300.csv')

    if not os.path.exists(os.path.dirname(fullpath)):
        try:
            os.makedirs(os.path.dirname(fullpath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    output          = open(fullpath, 'w')
    output.write(','.join(header) + '\n')

    directory       = ['data/20160513']
    for current_dir in directory :
        for afile in os.listdir(current_dir):
            source      = current_dir + '/' + afile
            print source

            data        = readFromFile(source)
            timestamp   = data[:,0]

            stimuli     = loadStimuli(source)
            stimuli_pos = findStimulus(timestamp, stimuli['time'])

            for stimulus_idx, stimulus_pos in enumerate(stimuli_pos) :
                iteree      = range(2, 16)

                if ((stimulus_pos + home_run) <= len(data[:,0])) :
                    for key, val in enumerate(iteree) :
                        current         = moveToAxis(data[:,val][stimulus_pos:(stimulus_pos + home_run)])
                        suspectedMax    = max(current[first_base:home_run])
                        averageBefore   = np.average(current[first_base:home_run])
                        percentageDiff  = countPercentageDifferent(suspectedMax, averageBefore)

                        if (key < (len(iteree) - 1)) :
                            output.write("{0:.2f},".format(percentageDiff))
                        else :
                            output.write("{0:.2f}".format(percentageDiff) + ',' + stimuli['direction'][stimulus_idx] + '\n')
if __name__ == "__main__":
    run()
    # print env_serial\
