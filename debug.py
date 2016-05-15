import os, sys, time, math, random, gevent
import numpy as np
import matplotlib.pyplot as plt

from preprocess import *

header      = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

def run() :
    start_time      = time.time()

    elapsed_time    = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
