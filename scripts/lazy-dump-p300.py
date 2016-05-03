import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import *

low_limit       = 5
high_limit      = 20
sampling_rate   = 129
split_amount    = 6

header          = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

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
    fullpath        = os.path.join('result', 'dump_p300.csv')

    if not os.path.exists(os.path.dirname(fullpath)):
        try:
            os.makedirs(os.path.dirname(fullpath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    output          = open(fullpath, 'w')

    directory       = ['data/20160503']

    for current_dir in directory :
        for file in os.listdir(current_dir):
            source      = current_dir + '/' + file
            # print source

            data            = readFromFile(source)
            timestamp       = data[:,0]

            stimulus_out    = loadStimulus(5.0)
            stimulus        = findStimulus(timestamp, stimulus_out, 6)

            direction       = file.split('_')[2]

            print source
            # print source + " " + str(len(stimulus))
            # print direction

            for i in range(2, 16) :
                current     = moveToAxis(data[:,i])
                parsed      = parse(current, split_amount)
                power       = countAllPower(parsed)
                diff        = findDifference(power)

                for val in stimulus :
                    if (len(diff) - (val)) > 8 :
                        output.write('%s,%s,' % (direction, header[i-2]))

                        diff_list   = []
                        for idx in range(3,10) :
                            if ((val + idx) < (len(diff) - 1)) :
                                output.write('%.2f,' % diff[val + idx])
                                diff_list.append(diff[val + idx])

                        if diff_list : output.write('%.2f,%.2f\n' % (np.amax(diff_list), np.mean(diff_list)))

if __name__ == "__main__":
    run()
    # print env_serial\
