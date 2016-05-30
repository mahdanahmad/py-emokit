import os, sys, time, math, random, gevent
import numpy as np
import matplotlib.pyplot as plt

from preprocess import *

first_base  = 18
home_run    = 192

header      = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

directory   = ['data/20160513']
plotIteree  = {}
plotRoot    = 'result/dump/'

def readFromFile(filename) :
    with open(filename) as afile :
        result = []
        for line in afile :
            # print line.split(',')
            splittedLine    = line.split(',')
            result.append([float(splittedLine[0])] +  map(int, splittedLine[1::1]))

        return np.array(result)

def loadStimuli(source) :
    stimuliPath = 'result/stimulus' + source.replace('data', '')
    with open(stimuliPath) as afile :
        result  = {
            'time'      : [],
            'direction' : []
        }
        for line in afile :
            splittedLine    = line.rstrip().split(',')
            result['time'].append(int(splittedLine[0]))
            result['direction'].append(splittedLine[1])

        return result

def run() :
    start_time      = time.time()

    folders         = ['data/parsed/transparent', 'data/parsed/whitebacked']
    for current_dir in folders :
        state       = current_dir.split('/')[2]
        for file in os.listdir(current_dir):
            source  = current_dir + '/' + file
            


    elapsed_time    = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
