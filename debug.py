import sys
import time
import matplotlib.pyplot as plt

from env import *
from datetime import datetime
from preprocess import *

low_limit       = 4
high_limit      = 30
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
    single      = single_data[:,9]

    centered    = doCentering(single)
    filtered    = doFiltering(centered, low_limit, high_limit, sampling_rate, 10)
    fft         = createFFT(filtered)
    psd         = createPSD(fft, sampling_rate)

    # plt.plot(single)
    # plt.title('Raw data')
    # plt.figure()
    # plt.plot(centered)
    # plt.title('Centered data')
    # plt.figure()
    # plt.plot(filtered)
    # plt.title('Filtered data')
    # plt.figure()
    # plt.plot(fft)
    # plt.title('FFT Result')
    # plt.figure()
    plt.plot(psd)
    plt.title('PSD Result')
    plt.show()

    # up_data     = readFromFile('data/8.5-up')
    # up          = up_data[:,9]
    #
    # stop_data   = readFromFile('data/10-stop')
    # stop        = stop_data[:,9]
    #
    # right_data  = readFromFile('data/12-right')
    # right       = right_data[:,9]
    #
    # left_data   = readFromFile('data/15-left')
    # left        = left_data[:,9]

    # splitted    = np.array_split(right, split_amount)
    #
    # splitted[:] = [doCentering(val) for val in splitted]
    # splitted[:] = [doFiltering(val, low_limit, high_limit, sampling_rate, 10) for val in splitted]
    # splitted[:] = [createFFT(val) for val in splitted]
    # splitted[:] = [createPSD(val, sampling_rate) for val in splitted]
    #
    # for key, val in enumerate(splitted):
    #     plt.plot(val)
    #     if (key < (len(splitted) - 1)) :
    #         plt.figure()
    #
    # plt.show()

    # centered_up     = doCentering(up)
    # centered_stop   = doCentering(stop)
    # centered_right  = doCentering(right)
    # centered_left   = doCentering(left)
    #
    # filtered_up     = doFiltering(centered_up, 4, 30, 129, 10)
    # filtered_stop   = doFiltering(centered_stop, 4, 30, 129, 10)
    # filtered_right  = doFiltering(centered_right, 4, 30, 129, 10)
    # filtered_left   = doFiltering(centered_left, 4, 30, 129, 10)
    #
    # fft_up          = createFFT(filtered_up)
    # fft_stop        = createFFT(filtered_stop)
    # fft_right       = createFFT(filtered_right)
    # fft_left        = createFFT(filtered_left)
    #
    # psd_up          = createPSD(fft_up, 129)
    # psd_stop        = createPSD(fft_stop, 129)
    # psd_right       = createPSD(fft_right, 129)
    # psd_left        = createPSD(fft_left, 129)
    #
    # plt.plot(psd_up)
    # plt.figure()
    # plt.plot(psd_stop)
    # plt.figure()
    # plt.plot(psd_right)
    # plt.figure()
    # plt.plot(psd_left)
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
