import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

from env import *

def initdummy() :
    with open('dummy-data') as afile :
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

def run() :
    start_time = time.time()

    data    = initdummy()
    first   = data[:,0]

    centered_first  = doCentering(first)
    filtered_first  = doFiltering(centered_first, 4, 20, 128, 5)
    fft_first       = createFFT(centered_first)
    psd_first       = createPSD(fft_first, 128)

    fft_first_wf    = createFFT(filtered_first)
    psd_first_wf    = createPSD(fft_first_wf, 128)

    # fp, perio       = signal.periodogram(fft_first, window='boxcar')
    # fw, welch       = signal.welch(fft_first, window='boxcar')

    elapsed_time = time.time() - start_time

    #plt.plot(np.fft.rfft(centered_first))
    #plt.show()
    # plt.plot(centered_first)
    # plt.figure()
    # plt.plot(filtered_first)
    # plt.figure()
    # plt.plot(fft_first)
    # plt.figure()
    # plt.plot(fft_first_wf)
    # plt.figure()
    # plt.plot(psd_first)
    # plt.figure()
    # plt.plot(psd_first_wf)
    # plt.figure()

    b, a = createButterBandpass(4, 20, 128, 10)

    # plt.plot(b, a)
    # plt.figure()

    w, h = signal.freqz(b, a)
    # plt.plot(w, 20 * np.log10(abs(h)))
    # plt.plot(w, abs(h))

    plt.plot((128 * 0.5 / np.pi) * w, 20 * np.log10(abs(h)))
    # plt.xscale('log')
    plt.title('Butterworth filter frequency response')
    plt.xlabel('Frequency [radians / second]')
    plt.ylabel('Amplitude [dB]')
    plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')
    plt.axvline(100, color='green') # cutoff frequency
    # plt.xlim([0, 100])
    # plt.plot()

    plt.show()

    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    # run()
    print env_serial
