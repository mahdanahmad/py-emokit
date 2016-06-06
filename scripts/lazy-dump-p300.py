import os, sys, math
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import *

try :
    first_base  = int(sys.argv[1])
except:
    first_base  = 18

try :
    home_run    = int(sys.argv[2])
except:
    home_run    = 65

lowcut          = 0
highcut         = 20
sampling_rate   = 128
order           = 10
passtype        = 'high'

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
# header      = [
#     "F3", "F3_pos",
#     "FC5", "FC5_pos",
#     "AF3", "AF3_pos",
#     "F7", "F7_pos",
#     "T7", "T7_pos",
#     "P7", "P7_pos",
#     "O1", "O1_pos",
#     "O2", "O2_pos",
#     "P8", "P8_pos",
#     "T8", "T8_pos",
#     "F8", "F8_pos",
#     "AF4", "AF4_pos",
#     "FC6", "FC6_pos",
#     "F4", "F4_pos",
#     "Direction"
# ]
# header      = ["F3", "FC5", "AF3", "F7", "T7", "P7", "O1", "O2", "P8", "T8", "F8", "AF4", "FC6", "F4", "Direction"]
header      = ["Fin", "FC", "AF", "Fout", "T", "P", "O", "Direction"]

couples     = [
    [0, 13], # F3 & F4
    [1, 12], # FC5 & FC6
    [2, 11], # AF3 & AF4
    [3, 10], # F7 & F8
    [4, 9],  # T7 & T8
    [5, 8],  # P7 & P8
    [6, 7]   # O1 & O2
]

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

    directory       = ['data/20160530']
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
                    channel_vals    = []
                    for key, val in enumerate(iteree) :
                        current         = moveToAxis(data[:,val][stimulus_pos:(stimulus_pos + home_run)])
                        current         = doFiltering(current, lowcut, highcut, sampling_rate, order, passtype)
                        suspectedMax    = max(current[first_base:])
                        positionMax     = np.argmax(current[first_base:])
                        averageBefore   = np.average(current[:first_base])

                        # max_peak        = countPercentageDifferent(suspectedMax, averageBefore)
                        max_peak        = suspectedMax - averageBefore

                        channel_vals.append(int(math.ceil(max_peak)))

                        # output['all'].write("{0:.2f},".format(max_peak) + str(positionMax) + ",")
                        # output[guinea].write("{0:.2f},".format(max_peak) + str(positionMax) + ",")

                    for val in couples :
                        left_side   = val[0]
                        right_side  = val[1]
                        difference  = channel_vals[left_side] - channel_vals[right_side]

                        output['all'].write("{0:.2f},".format(difference))
                        output[guinea].write("{0:.2f},".format(difference))

                    output['all'].write(stimuli['direction'][stimulus_idx] + '\n')
                    output[guinea].write(stimuli['direction'][stimulus_idx] + '\n')

if __name__ == "__main__":
    run()
    # print env_serial\
