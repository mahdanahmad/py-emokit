import sys
import time
import numpy as np
import matplotlib.pyplot as plt

from env import *
from datetime import datetime
from preprocess import *

low_limit       = 5
high_limit      = 20
split_amount    = 6
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
    data    = readFromFile(source)

    channel = []
    for i in range(2, 16)   :
        current     = moveToAxis(data[:,i])
        filtered    = doFiltering(current, 0, 8, 129)
        parsed      = parse(current, split_amount)
        power       = countAllPower(parsed)
        diff        = findDifference(power)

        plt.plot(diff)
        plt.title(header[i - 2])
        if (i is not 15) : plt.figure()

    plt.show()

if __name__ == "__main__":
    run()
