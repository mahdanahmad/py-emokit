import sys
import time
import numpy as np
import matplotlib.pyplot as plt

from env import *
from datetime import datetime
from preprocess import *

low_limit       = 5
high_limit      = 20
split_amount    = 5
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
            result.append(map(int, line.split(',')))

        return np.array(result)

def run() :
    start_time  = time.time()

    # print source


    single_data = readFromFile(source)

    data        = []
    occipital   = []
    # data        = single_data
    for i in range(2, 16)   : data.append(single_data[:,i])
    for i in range(8, 10)   : occipital.append(single_data[:,i])

    data[:]         = [doCentering(val) for val in data]
    # data[:]         = [doFiltering(val, low_limit, high_limit, sampling_rate, 10) for val in data]
    # data[:]         = [createFFT(val) for val in data]
    # data[:]         = [createPSD(val, sampling_rate) for val in data]

    for key, val in enumerate(data):
        plt.plot(val)
        plt.title(header[key] + str(key + 1))
        if (key < len(data) - 1) : plt.figure()

    plt.show()

    # occipital[:]    = [doCentering(val) for val in occipital]
    # occipital[:]    = [doFiltering(val, low_limit, high_limit, sampling_rate, 10) for val in occipital]
    # occipital[:]    = [createFFT(val) for val in occipital]
    # occipital[:]    = [createPSD(val, sampling_rate) for val in occipital]

    # for key, val in enumerate(occipital):
    #     plt.plot(val)
    #     plt.title('O' + str(key + 1))
    #     plt.figure()

    # plt.show()

    # O1      = np.array_split(occipital[0], 8)
    # O1[:]   = [doCentering(val) for val in O1]
    # O1[:]   = [doFiltering(val, low_limit, high_limit, sampling_rate, 10) for val in O1]
    # O1[:]   = [createFFT(val) for val in O1]
    # O1[:]   = [createPSD(val, sampling_rate) for val in O1]
    #
    # for key, val in enumerate(O1):
    #     if (key < len(O1) - 1) :
    #         plt.plot(val)
    #         plt.title('O1 detik ke-' + str(key + 1))
    #         if (key < len(O1) - 2) : plt.figure()
    #
    # plt.show()
    #
    # O2      = np.array_split(occipital[1], 8)
    # O2[:]   = [doCentering(val) for val in O2]
    # O2[:]   = [doFiltering(val, low_limit, high_limit, sampling_rate, 10) for val in O2]
    # O2[:]   = [createFFT(val) for val in O2]
    # O2[:]   = [createPSD(val, sampling_rate) for val in O2]
    #
    # for key, val in enumerate(O2):
    #     if (key < len(O2) - 1) :
    #         plt.plot(val)
    #         plt.title('O2 detik ke-' + str(key + 1))
    #         if (key < len(O2) - 2) : plt.figure()
    #
    # plt.show()
    # b, a = createButterBandpass(4, 20, 128, 10)
    #
    # # plt.plot(b, a)
    # # plt.figure()
    #
    # w, h = signal.freqz(b, a)
    # # plt.plot(w, 20 * np.log10(abs(h)))
    # # plt.plot(w, abs(h))
    #
    # plt.plot((128 * 0.5 / np.pi) * w, 20 * np.log10(abs(h)))
    # # plt.xscale('log')
    # plt.title('Butterworth filter frequency response')
    # plt.xlabel('Frequency [radians / second]')
    # plt.ylabel('Amplitude [dB]')
    # plt.margins(0, 0.1)
    # plt.grid(which='both', axis='both')
    # plt.axvline(100, color='green') # cutoff frequency
    # # plt.xlim([0, 100])
    # # plt.plot()

    # plt.show()

    elapsed_time = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
