import os, sys, math
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import *

sampling_rate   = 129

try :
    source      = sys.argv[1]
except:
    # source      = 'data/10-stop'
    source      = 'data/20160503/174424_p300_stop_20.csv'

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

    stimulus_single = (int)(sampling_rate / 3)
    first_cut       = stimulus[0] - stimulus_single
    second_cut      = stimulus[0] + sampling_rate
    sampling        = (1000 / sampling_rate)
    for i in range(2, 16) :
        current         = moveToAxis(data[:,i])
        first_stimulus  = current[first_cut:second_cut]
        x               = np.arange(len(first_stimulus))

        plt.plot(x * sampling , first_stimulus)

        plt.xlabel('Time [ms]')
        plt.ylabel('Power')

        # plt.axvline(x=(stimulus_single * sampling), color='r', ls='--')
        # plt.axvline(x=((stimulus_single * sampling) + 140), color='g', ls='--')
        # plt.axvline(x=((stimulus_single * sampling) + 500), color='g', ls='--')
        plt.axvline(x=0, color='r', ls='--')
        plt.axvline(x=140, color='g', ls='--')
        plt.axvline(x=500, color='g', ls='--')

        first_base      = (int)(stimulus_single + math.floor(sampling_rate * 0.14))
        end_game        = (int)(stimulus_single + math.ceil(sampling_rate * 0.50))

        suspectedPower  = countPower(first_stimulus[first_base:end_game])
        totalPower      = countPower(first_stimulus[stimulus_single:end_game])
        percentage      = (suspectedPower * 100) / totalPower

        plt.title("{0:.2f}%".format(percentage))

        if (i < 15) : plt.figure()

    plt.show()

if __name__ == "__main__":
    run()
    # print env_serial\
