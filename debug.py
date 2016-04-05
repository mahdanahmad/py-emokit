import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

from env import *
from datetime import datetime

low_limit       = 4
high_limit      = 30
split_amount    = 5
sampling_rate   = 129

def initdummy() :
    with open('dummy-data') as afile :
        result = []
        for line in afile :
            result.append(map(int, line.split(',')))

        return np.array(result)

def readFromFile(filename) :
    with open(filename) as afile :
        result = []
        for line in afile :
            result.append(map(int, line.split(',')))

        return np.array(result)

def doCentering(data) :
    return data - data.mean()

def createButterBandpass(lowcut, highcut, fs, order = 10) :
    nyq = 0.5 * fs

    low = lowcut / nyq
    high = highcut / nyq

    return signal.butter(order, [low, high], btype='band')

def doFiltering(data, lowcut, highcut, fs, order = 10) :
    b, a = createButterBandpass(lowcut, highcut, fs, order)
    y = signal.lfilter(b, a, data)

    return y

def createFFT(data) :
    return np.fft.rfft(data)

def createPSD(data, fs = 128) :
    conj        = np.conjugate(data)
    onesided    = conj * data

    periode     = onesided.size / (fs / 2)

    temp        = []
    length      = 9999
    for idx in range(periode):
        temp.append(onesided[0+idx::periode])
        if (length > onesided[0+idx::periode].size) :
            length = onesided[0+idx::periode].size

    total = np.zeros((length), dtype=np.complex128)

    for idx in range(periode):
        total += np.array(temp[idx])[:length:]

    return total / periode

def split(data, amount) :
    index       = data.size / amount
    indices     = np.arange(index, index * amount, index)

    # print indices

    return np.split(data, indices)

def run() :
    start_time  = time.time()

    up_data     = readFromFile('data/8.5-up')
    up          = up_data[:,9]

    stop_data   = readFromFile('data/10-stop')
    stop        = stop_data[:,9]

    right_data  = readFromFile('data/12-right')
    right       = right_data[:,9]

    left_data   = readFromFile('data/15-left')
    left        = left_data[:,9]

    # splitted    = split(right, split_amount)
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

    centered_up     = doCentering(up)
    centered_stop   = doCentering(stop)
    centered_right  = doCentering(right)
    centered_left   = doCentering(left)

    filtered_up     = doFiltering(centered_up, 4, 30, 129, 10)
    filtered_stop   = doFiltering(centered_stop, 4, 30, 129, 10)
    filtered_right  = doFiltering(centered_right, 4, 30, 129, 10)
    filtered_left   = doFiltering(centered_left, 4, 30, 129, 10)

    fft_up          = createFFT(filtered_up)
    fft_stop        = createFFT(filtered_stop)
    fft_right       = createFFT(filtered_right)
    fft_left        = createFFT(filtered_left)

    psd_up          = createPSD(fft_up, 129)
    psd_stop        = createPSD(fft_stop, 129)
    psd_right       = createPSD(fft_right, 129)
    psd_left        = createPSD(fft_left, 129)

    plt.plot(psd_up)
    plt.figure()
    plt.plot(psd_stop)
    plt.figure()
    plt.plot(psd_right)
    plt.figure()
    plt.plot(psd_left)
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
    # run()
    # print env_serial\
