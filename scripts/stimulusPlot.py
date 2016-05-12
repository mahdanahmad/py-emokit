import os, sys, math
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import *

sampling_rate   = 129

header          = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

try :
    source      = sys.argv[1]
except:
    # source      = 'data/20160503/174424_p300_stop_20.csv'
    # source      = 'data/20160503/175805_p300_forward_20.csv'
    # source      = 'data/20160503/180853_p300_left_20.csv'
    # source      = 'data/20160503/181835_p300_right_20.csv'
    source      = [
        'data/20160503/174424_p300_stop_20.csv',
        'data/20160503/175805_p300_forward_20.csv',
        'data/20160503/180853_p300_left_20.csv',
        'data/20160503/181835_p300_right_20.csv'
    ]

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

# def run() :
def run(source) :
    direction       = source.split('_')[2]
    fullpath        = os.path.join('result', 'dump_' + direction + '.csv')

    if not os.path.exists(os.path.dirname(fullpath)):
        try:
            os.makedirs(os.path.dirname(fullpath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # output          = open(fullpath, 'w')
    # output.write("F3,FC5,AF3,F7,T7,P7,O1,O2,P8,T8,F8,AF4,FC6,F4\n")

    data            = readFromFile(source)
    timestamp       = data[:,0]

    stimulus_out    = loadStimulus(5.0)
    stimulus        = findStimulus(timestamp, stimulus_out)

    print stimulus

    # stimulus_single = (int)(sampling_rate / 3)
    stimulus_single = 0
    sampling        = (1000 / sampling_rate)
    for key, val in enumerate(stimulus) :
        first_cut       = val - stimulus_single
        second_cut      = val + sampling_rate

        if (first_cut < 0) : first_cut = 0

        iteree      = range(2, 16)

        for idx, i in enumerate(iteree) :
            current         = moveToAxis(data[:,i])

            if (len(current) >= second_cut) :
                first_stimulus  = moveToAxis(current[first_cut:second_cut])
                x               = np.arange(len(first_stimulus))

                plt.plot((x - stimulus_single) * sampling , first_stimulus)

                plt.xlabel('Time [ms]')
                plt.ylabel('Voltage')

                # plt.axvline(x=(stimulus_single * sampling), color='r', ls='--')
                # plt.axvline(x=((stimulus_single * sampling) + 140), color='g', ls='--')
                # plt.axvline(x=((stimulus_single * sampling) + 500), color='g', ls='--')
                plt.axvline(x=0, color='r', ls='--')
                plt.axvline(x=140, color='g', ls='--')
                plt.axvline(x=500, color='g', ls='--')

                first_base      = (int)(stimulus_single + math.floor(sampling_rate * 0.14))
                end_game        = (int)(stimulus_single + math.ceil(sampling_rate * 0.50))

                suspectedMax    = max(first_stimulus[first_base:end_game])
                averageBefore   = np.average(first_stimulus[stimulus_single:end_game])

                somewhatNow     = countPercentageDifferent(suspectedMax, averageBefore)
                # print header[idx] + ' ' + str(suspectedMax) + ' | ' + str(averageBefore) + ' => {0:.2f}%'.format(somewhatNow)

                plt.title("{0:.2f}%".format(somewhatNow))

                if (idx < (len(iteree) - 1)) :
                    # output.write("{0:.2f},".format(percentage))
                    plt.figure()
                else :
                    # output.write("{0:.2f}\n".format(percentage))
                    # plt.show()
                    pass

                # print len(first_stimulus[first_base:end_game])
                # print len(first_stimulus[stimulus_single:end_game])

if __name__ == "__main__":
    run(source[3])
    # for val in source : run(val)
