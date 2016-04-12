import sys
import time
import matplotlib.pyplot as plt

from env import *
from datetime import datetime
from preprocess import *

low_limit       = 5
high_limit      = 20
split_amount    = 5
sampling_rate   = 129

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
    data.append(single_data[:,8])
    data.append(single_data[:,9])

    data[:] = [doCentering(val) for val in data]
    data[:] = [doFiltering(val, low_limit, high_limit, sampling_rate, 10) for val in data]
    data[:] = [createFFT(val) for val in data]
    data[:] = [createPSD(val, sampling_rate) for val in data]

    for key, val in enumerate(data):
        plt.plot(val)
        if (key < (len(data) - 1)) :
            plt.figure()

    plt.show()

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
