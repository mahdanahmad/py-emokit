import os, sys, time, math, random, gevent
import numpy as np
import matplotlib.pyplot as plt

from scipy import signal
from preprocess import *

source  = 'data/10-stop'

low_limit       = 5
high_limit      = 15
sampling_rate   = 128

# np.set_printoptions(precision=3)

start_sec       = 5
end_sec         = 6

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
    # print data

    # O1          = data[:,8]
    O2          = data[(sampling_rate * start_sec):(sampling_rate * end_sec),9]
    # print O1
    # print 'Raw Data'
    # print O2
    # print ''
    # print ''

    x           = np.arange(len(O2))

    plt.plot((x * 1000 / sampling_rate), O2)
    plt.title('Raw Data')
    plt.xlabel('Time [ms]')
    plt.ylabel(u'Voltage [\u00B5V]')
    plt.figure()

    # centered_O1 = doCentering(O1)
    centered_O2 = doCentering(O2)
    print 'Centered'
    print centered_O2
    print ''
    print ''

    plt.plot((x * 1000 / sampling_rate), centered_O2)
    plt.title('Centered Data')
    plt.xlabel('Time [ms]')
    plt.ylabel(u'Voltage [\u00B5V]')
    plt.figure()

    # filtered_O1 = doFiltering(centered_O1, low_limit, high_limit, sampling_rate)
    filtered_O2 = doFiltering(centered_O2, low_limit, high_limit, sampling_rate)
    print 'Filtered'
    print filtered_O2
    print ''
    print ''

    plt.plot((x * 1000 / sampling_rate), filtered_O2)
    plt.title('Filtered Data')
    plt.xlabel('Time [ms]')
    plt.ylabel(u'Voltage [\u00B5V]')
    plt.figure()

    # fft_O1      = createFFT(filtered_O1)
    fft_O2      = createFFT(filtered_O2)
    print 'FFT'
    print fft_O2
    print ''
    print ''

    plt.plot(fft_O2)
    plt.title('FFT Result')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel(u'Voltage [\u00B5V]')
    plt.figure()

    fw, PSDw    = signal.welch(filtered_O2, sampling_rate)
    print 'Welch'
    print PSDw
    print ''
    print ''

    # plt.semilogy(fw, PSDw)
    # plt.xlabel('Frequency [Hz]')
    # plt.ylabel('PSD [W/Hz]')
    # plt.figure()

    plt.plot(fw, PSDw)
    plt.title('Welch\'s method Result')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [pW/Hz]')
    plt.figure()

    fp, PSDp    = signal.periodogram(filtered_O2, sampling_rate)
    print 'Periodogram'
    print PSDp
    print ''
    print ''

    plt.plot(fp, PSDp)
    plt.title('Periodogram Result')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [pW/Hz]')
    plt.figure()


    # psd_O1      = createPSD(fft_O1, sampling_rate)
    psd_O2      = createPSD(fft_O2, sampling_rate)
    print 'PSD'
    print psd_O2
    print ''
    print ''

    plt.plot(psd_O2)
    plt.title('PSD Result')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Power [pW]')
    # plt.figure()

    # plt.plot(psd_O2)
    # plt.title('PSD Result')
    # plt.show()

    # plt.plot(psd_O1)
    # plt.figure()
    # plt.plot(psd_O2)
    # plt.show()

if __name__ == "__main__":
    run()
