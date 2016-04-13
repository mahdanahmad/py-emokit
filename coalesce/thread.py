#!/usr/bin/python

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID   = threadID
        self.name       = name
        self.delay      = delay
        self.counter    = 5
    def run(self):
        print "Starting " + self.name
        self.print_time()
        print "Exiting " + self.name

    def print_time(self):
        while self.counter:
            if exitFlag:
                self.name.exit()
            time.sleep(self.delay)
            print "%s: %s" % (self.name, time.ctime(time.time()))
            self.counter -= 1

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()
