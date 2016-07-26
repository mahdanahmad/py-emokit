import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import *

low_limit       = 5
high_limit      = 20
sampling_rate   = 129
split_amount    = 6

first_base      = 18
home_run        = 65

limit_paek      = 72.30

header          = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4","Direction","Guinea"]

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
    result  = {
        'all' : {
            'left'      : {'F3' : 0, 'FC5' : 0, 'AF3' : 0, 'F7' : 0, 'T7' : 0, 'P7' : 0, 'O1' : 0, 'O2' : 0, 'P8' : 0, 'T8' : 0, 'F8' : 0, 'AF4' : 0, 'FC6' : 0, 'F4' : 0},
            'stop'      : {'F3' : 0, 'FC5' : 0, 'AF3' : 0, 'F7' : 0, 'T7' : 0, 'P7' : 0, 'O1' : 0, 'O2' : 0, 'P8' : 0, 'T8' : 0, 'F8' : 0, 'AF4' : 0, 'FC6' : 0, 'F4' : 0},
            'right'     : {'F3' : 0, 'FC5' : 0, 'AF3' : 0, 'F7' : 0, 'T7' : 0, 'P7' : 0, 'O1' : 0, 'O2' : 0, 'P8' : 0, 'T8' : 0, 'F8' : 0, 'AF4' : 0, 'FC6' : 0, 'F4' : 0},
            'forward'   : {'F3' : 0, 'FC5' : 0, 'AF3' : 0, 'F7' : 0, 'T7' : 0, 'P7' : 0, 'O1' : 0, 'O2' : 0, 'P8' : 0, 'T8' : 0, 'F8' : 0, 'AF4' : 0, 'FC6' : 0, 'F4' : 0},
        }
    }

    directory       = ['data/20160513']
    for current_dir in directory :
        for afile in os.listdir(current_dir):
            source      = current_dir + '/' + afile
            guinea      = source.split('_')[1]
            print source

            if guinea not in result :
                result[guinea]  = {
                    'left'      : {'F3' : 0, 'FC5' : 0, 'AF3' : 0, 'F7' : 0, 'T7' : 0, 'P7' : 0, 'O1' : 0, 'O2' : 0, 'P8' : 0, 'T8' : 0, 'F8' : 0, 'AF4' : 0, 'FC6' : 0, 'F4' : 0},
                    'stop'      : {'F3' : 0, 'FC5' : 0, 'AF3' : 0, 'F7' : 0, 'T7' : 0, 'P7' : 0, 'O1' : 0, 'O2' : 0, 'P8' : 0, 'T8' : 0, 'F8' : 0, 'AF4' : 0, 'FC6' : 0, 'F4' : 0},
                    'right'     : {'F3' : 0, 'FC5' : 0, 'AF3' : 0, 'F7' : 0, 'T7' : 0, 'P7' : 0, 'O1' : 0, 'O2' : 0, 'P8' : 0, 'T8' : 0, 'F8' : 0, 'AF4' : 0, 'FC6' : 0, 'F4' : 0},
                    'forward'   : {'F3' : 0, 'FC5' : 0, 'AF3' : 0, 'F7' : 0, 'T7' : 0, 'P7' : 0, 'O1' : 0, 'O2' : 0, 'P8' : 0, 'T8' : 0, 'F8' : 0, 'AF4' : 0, 'FC6' : 0, 'F4' : 0},
                }

            data        = readFromFile(source)
            timestamp   = data[:,0]

            stimuli     = loadStimuli(source)
            stimuli_pos = findStimulus(timestamp, stimuli['time'])

            for stimulus_idx, stimulus_pos in enumerate(stimuli_pos) :
                iteree      = range(2, 16)
                direction   = stimuli['direction'][stimulus_idx]

                if ((stimulus_pos + home_run) <= len(data[:,0])) :
                    for key, val in enumerate(iteree) :
                        current         = moveToAxis(data[:,val][stimulus_pos:(stimulus_pos + home_run)])
                        # suspectedMax    = max(current[first_base:home_run])
                        # averageBefore   = np.average(current[first_base:home_run])
                        # percentageDiff  = countPercentageDifferent(suspectedMax, averageBefore)


                        suspectedPower  = countPower(current[first_base:home_run])
                        totalPower      = countPower(current[:home_run])
                        percentageDiff  = (suspectedPower * 100) / totalPower

                        if (percentageDiff > limit_paek) : result['all'][direction][header[key]] += 1
                        if (percentageDiff > limit_paek) : result[guinea][direction][header[key]] += 1

                        # if (key < (len(iteree) - 1)) :
                        #     output['all'].write("{0:.2f},".format(percentageDiff))
                        #     output[guinea].write("{0:.2f},".format(percentageDiff))
                        # else :
                        #     output['all'].write("{0:.2f}".format(percentageDiff) + ',' + stimuli['direction'][stimulus_idx] + '\n')
                        #     output[guinea].write("{0:.2f}".format(percentageDiff) + ',' + stimuli['direction'][stimulus_idx] + '\n')

    fullpath        = os.path.join('result/dump_p300_pos.csv')

    if not os.path.exists(os.path.dirname(fullpath)):
        try:
            os.makedirs(os.path.dirname(fullpath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    output          = open(fullpath, 'w')
    output.write(','.join(header) + '\n')

    for (key, val) in result.iteritems() :
        for (keykey, valval) in val.iteritems() :
            for channel in header[:14] :
                output.write(str(valval[channel]) + ',')

            output.write(keykey + ',')
            output.write(key + '\n')

if __name__ == "__main__":
    run()
    # print env_serial\
