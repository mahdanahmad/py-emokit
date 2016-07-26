import os, sys, time, math, random, gevent, string
import numpy as np


from preprocess import *

all             = string.maketrans('','')
nodigs          = all.translate(all, string.digits)

source_dir      = 'data/forTables'

low_limit       = 5
high_limit      = 15
sampling_rate   = 129

result          = {
    '9'     : {
        'nice'      : 0,
        'left'      : 0,
        'right'     : 0,
        'sad'       : 0,
    },
    '10'    : {
        'nice'      : 0,
        'left'      : 0,
        'right'     : 0,
        'sad'       : 0,
    },
    '11'    : {
        'nice'      : 0,
        'left'      : 0,
        'right'     : 0,
        'sad'       : 0,
    },
    '12'    : {
        'nice'      : 0,
        'left'      : 0,
        'right'     : 0,
        'sad'       : 0,
    },
}

def readFromFile(filename) :
    with open(filename) as afile :
        result = []
        for line in afile :
            # print line.split(',')
            splittedLine    = line.split(',')
            result.append([float(splittedLine[0])] +  map(int, splittedLine[1::1]))

        return np.array(result)

def run() :
    for file in os.listdir(source_dir):
        source      = source_dir + '/' + file
        print source

        guinea      = file.split('_')[1].translate(all, nodigs)
        print guinea

        data        = readFromFile(source)
        O1          = chainSSVEP(data[:,8], sampling_rate, low_limit, high_limit)
        O2          = chainSSVEP(data[:,9], sampling_rate, low_limit, high_limit)

        if (O1 == O2) :
            result[guinea]['nice'] = result[guinea]['nice'] + 1;
        elif (O1 > O2) :
            result[guinea]['left'] = result[guinea]['left'] + 1;
        elif (O1 < O2) :
            result[guinea]['right'] = result[guinea]['right'] + 1;
        else :
            result[guinea]['sad'] = result[guinea]['sad'] + 1;


    print result


if __name__ == "__main__":
    run()
