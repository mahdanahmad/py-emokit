import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import *

try :
    first_base  = int(sys.argv[1])
except:
    first_base  = 33

try :
    home_run    = int(sys.argv[2])
except:
    home_run    = 128

# header      = [
#     "min_F3", "max_F3",
#     "min_FC5", "max_FC5",
#     "min_AF3", "max_AF3",
#     "min_F7", "max_F7",
#     "min_T7", "max_T7",
#     "min_P7", "max_P7",
#     "min_O1", "max_O1",
#     "min_O2", "max_O2",
#     "min_P8", "max_P8",
#     "min_T8", "max_T8",
#     "min_F8", "max_F8",
#     "min_AF4", "max_AF4",
#     "min_FC6", "max_FC6",
#     "min_F4", "max_F4",
#     "Guinea", "Direction"
# ]
header      = ["F3", "FC5", "AF3", "F7", "T7", "P7", "O1", "O2", "P8", "T8", "F8", "AF4", "FC6", "F4", "Direction"]

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
    fullpath        = os.path.join('result/dump_p300', 'forthename' + str(first_base) + '-' + str(home_run) + '.csv')

    if not os.path.exists(os.path.dirname(fullpath)):
        try:
            os.makedirs(os.path.dirname(fullpath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    output          = {}
    output['all']   = open(fullpath.replace('forthename', 'all'), 'w')
    output['all'].write(','.join(header) + '\n')

    directory       = ['data/20160513']
    for current_dir in directory :
        for afile in os.listdir(current_dir):
            source      = current_dir + '/' + afile
            guinea      = source.split('_')[1]
            print source

            if not os.path.isfile(fullpath.replace('forthename', guinea)) :
                output[guinea]  = open(fullpath.replace('forthename', guinea), 'w')
                output[guinea].write(','.join(header) + '\n')

            data        = readFromFile(source)
            timestamp   = data[:,0]

            stimuli     = loadStimuli(source)
            stimuli_pos = findStimulus(timestamp, stimuli['time'])

            for stimulus_idx, stimulus_pos in enumerate(stimuli_pos) :
                iteree      = range(2, 16)

                if ((stimulus_pos + home_run) <= len(data[:,0])) :
                    for key, val in enumerate(iteree) :
                        current         = moveToAxis(data[:,val][stimulus_pos:(stimulus_pos + home_run)])
                        suspectedMax    = max(current[first_base:])
                        suspectedMin    = min(current[first_base:])
                        averageBefore   = np.average(current[:first_base])

                        max_peax        = countPercentageDifferent(suspectedMax, averageBefore)
                        min_peax        = countPercentageDifferent(suspectedMin, averageBefore)

                        if (key < (len(iteree) - 1)) :
                            # output[guinea].write("{0:.2f},".format(min_peax) + "{0:.2f},".format(max_peax))
                            output['all'].write("{0:.2f},".format(max_peax))
                            output[guinea].write("{0:.2f},".format(max_peax))
                        else :
                            # output[guinea].write("{0:.2f},".format(min_peax) + "{0:.2f},".format(max_peax) + guinea + ',' + stimuli['direction'][stimulus_idx] + '\n')
                            output['all'].write("{0:.2f},".format(max_peax) + stimuli['direction'][stimulus_idx] + '\n')
                            output[guinea].write("{0:.2f},".format(max_peax) + stimuli['direction'][stimulus_idx] + '\n')
if __name__ == "__main__":
    run()
    # print env_serial\
