import os, sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import *

low_limit       = 5
high_limit      = 15
sampling_rate   = 129

header          = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

def readFromFile(filename) :
    with open(filename) as afile :
        result = []
        for line in afile :
            # print line.split(',')
            splittedLine    = line.split(',')
            result.append([float(splittedLine[0])] +  map(int, splittedLine[1::1]))

        return np.array(result)

def run() :
    fullpath    = os.path.join('result', 'dump_ssvep.csv')

    if not os.path.exists(os.path.dirname(fullpath)):
        try:
            os.makedirs(os.path.dirname(fullpath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    output      = open(fullpath, 'w')

    directory   = ['data/20160408', 'data/20160411', 'data/20160412']

    for current_dir in directory :
        for file in os.listdir(current_dir):
            source      = current_dir + '/' + file
            data        = readFromFile(source)

            print source

            O1          = data[:,8]
            centered_O1 = doCentering(O1)
            filtered_O1 = doFiltering(centered_O1, low_limit, high_limit, sampling_rate)
            fft_O1      = createFFT(filtered_O1)
            psd_O1      = createPSD(fft_O1, sampling_rate)
            max_O1      = np.argmax(psd_O1)

            O2          = data[:,9]
            centered_O2 = doCentering(O2)
            filtered_O2 = doFiltering(centered_O2, low_limit, high_limit, sampling_rate)
            fft_O2      = createFFT(filtered_O2)
            psd_O2      = createPSD(fft_O2, sampling_rate)
            max_O2      = np.argmax(psd_O2)

            output.write("%s,%s,%s\n" % (source, max_O1, max_O2))

if __name__ == "__main__":
    run()
    # print env_serial\
