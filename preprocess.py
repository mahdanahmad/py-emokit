import numpy as np
import scipy.signal as signal

def doCentering(data) :
    data        = np.array(data)

    return data - data.mean()

def createButterBandpass(lowcut, highcut, fs, order = 10) :
    nyq         = 0.5 * fs

    low         = lowcut / nyq
    high        = highcut / nyq

    return signal.butter(order, [low, high], btype='band')

def doFiltering(data, lowcut, highcut, fs, order = 10) :
    b, a        = createButterBandpass(lowcut, highcut, fs, order)
    y           = signal.lfilter(b, a, data)

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

def moveToAxis(data) :
    data        = np.array(data)

    return data - data.min()

def parse(data, split_amount) :
    reminder    = data
    result      = []

    while len(reminder) > split_amount:
        result.append(reminder[0:split_amount])
        reminder    = reminder[split_amount:]

    return result

def countPower(data) :
    return np.sum(np.square(data))

def countAllPower(data) :
    result  = []
    for val in data : result.append(countPower(val))

    return result

def countPercentageDifferent(newValue, oldValue) :
    return (newValue - oldValue) * 100 / oldValue

def findDifference(data) :
    result  = []
    for key, val in enumerate(data) :
        if (key is not 0) :
            result.append(countPercentageDifferent(val, data[key - 1]))

    return result

def chainSSVEP(data, fs, lowcut, highcut) :
    result  = doCentering(data)
    result  = doFiltering(result, lowcut, highcut, fs)
    result  = createFFT(result)
    result  = createPSD(result, fs)

    return result
