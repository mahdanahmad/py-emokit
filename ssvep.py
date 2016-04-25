import sys
import time
import numpy as np
import matplotlib.pyplot as plt

from env import *
from random import randint
from datetime import datetime
from preprocess import *

low_limit       = 5
high_limit      = 15
sampling_rate   = 129

header          = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

try :
    source      = sys.argv[1]
except:
    source      = 'data/10-stop'

def readFromFile(filename) :
    with open(filename) as afile :
        result = []
        for line in afile :
            # print line.split(',')
            splittedLine    = line.split(',')
            result.append([float(splittedLine[0])] +  map(int, splittedLine[1::1]))

        return np.array(result)

def run() :
    data        = readFromFile(source)

    O1          = data[:,8]
    O2          = data[:,9]

    plt.plot(O2)
    plt.figure()

    centered_O1 = doCentering(O1)
    centered_O2 = doCentering(O2)

    # plt.plot(centered_O2)
    # plt.title('Centered Signal')
    # plt.figure()

    filtered_O1 = doFiltering(centered_O1, low_limit, high_limit, sampling_rate)
    filtered_O2 = doFiltering(centered_O2, low_limit, high_limit, sampling_rate)

    # plt.plot(filtered_O2)
    # plt.title('Filtered Signal')
    # plt.figure()

    fft_O1      = createFFT(filtered_O1)
    fft_O2      = createFFT(filtered_O2)

    # plt.plot(fft_O2)
    # plt.title('FFT Result')
    # plt.figure()

    psd_O1      = createPSD(fft_O1, sampling_rate)
    psd_O2      = createPSD(fft_O2, sampling_rate)

    

    # plt.plot(psd_O2)
    # plt.title('PSD Result')
    # plt.show()

    # plt.plot(psd_O1)
    # plt.figure()
    # plt.plot(psd_O2)
    # plt.show()

if __name__ == "__main__":
    run()
    # print env_serial\
