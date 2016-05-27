import os, sys, time, math, random, gevent
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image, ImageFont, ImageDraw
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import *

folders     = ['data/20160513']

header      = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

font        = ImageFont.truetype("FreeSans.ttf", 28)
imagepath   = 'images/coalesce/base.jpg'

files_amn   = 10
stimuli_amn = 20
grouped_val = True

first_base  = 33
home_run    = 128
radius      = 26
outline     = 3
line_color  = (0,0,0)
text_color  = (255,255,255)

5"P7",6"O1",7"O2",8"P8"


position    = [
    [233, 210], # F3
    [135, 282], # FC5
    [170, 138], # AF3
    [88, 229],  # F7
    [57, 356],  # T7
    [144, 540], # P7
    [225, 625], # O1
    [372, 625], # O2
    [447, 540], # P8
    [538, 356], # T8
    [509, 229], # F8
    [419, 137], # AF4
    [455, 282], # FC6
    [352, 210]  # F4
]

couples     = [
    [0, 13], # F3 & F4
    [1, 12], # FC5 & FC6
    [2, 11], # AF3 & AF4
    [3, 10], # F7 & F8
    [4, 9],  # T7 & T8
    [5, 8],  # P7 & P8
    [6, 7]   # O1 & O2
]

dir_counter = { 'left' : 1, 'right' : 1, 'forward' : 1, 'stop' : 1 }

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

def findFiles(folderpath, grouped=False) :
    result  = []
    for current_dir in folderpath :
        for file in os.listdir(current_dir):
            result.append(current_dir + '/' + file)

    if grouped :
        grouped_result  = {}
        for val in result :
            name    = val.split('_')[1]

            if name not in grouped_result : grouped_result[name] = []
            grouped_result[name].append(val)

        return grouped_result
    else :
        return result

def randomPick(fileList, count=10, grouped=False) :
    if grouped :
        result  = []
        each    = int(math.ceil(count / len(fileList)))
        for key, val in fileList.iteritems() :
            if (len(val) > each) :
                temp    = random.sample(val, each)
            else :
                temp    = val

            result += temp

        return result
    else :
        if (len(fileList) > count) :
            return random.sample(fileList, count)
        else :
            return fileList

def randomStimulus(stimuli, count=10, grouped=False) :
    if grouped :
        grouped     = {}
        for key, val in enumerate(stimuli['direction']) :
            if val not in grouped : grouped[val] = []
            grouped[val].append(stimuli['time'][key])

        result      = {
            'time'      : [],
            'direction' : []
        }
        each        = int(math.ceil(count / len(grouped)))
        for key, val in grouped.iteritems() :
            if (len(val) > each) :
                temp    = random.sample(val, each)
            else :
                temp    = val

            for ran in temp :
                result['time'].append(ran)
                result['direction'].append(key)

    else :
        converted   = {}
        for key, val in enumerate(stimuli['time']) : converted[val] = stimuli['direction'][key]
        randomed    = random.sample(converted.items(), count)

        result  = {
            'time'      : [],
            'direction' : []
        }
        for val in randomed :
            result['time'].append(val[0])
            result['direction'].append(val[1])

    sorted_result   = zip(*sorted(zip(result['time'], result['direction'])))
    return {
        'time'      : sorted_result[0],
        'direction' : sorted_result[1]
    }

def saveImage(canvas, direction) :
    output_path = "result/dump_visual/" + direction + "_" + str(dir_counter[direction]) + ".jpg"
    dir_counter[direction] += 1

    print output_path

    if not os.path.exists(os.path.dirname(output_path)):
        try:
            os.makedirs(os.path.dirname(output_path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    canvas.save(output_path, "JPEG", quality=100, optimize=True, progressive=True)

def putChannel(canvas, data, stimulus_pos, iteree, direction) :
    addition        = ImageDraw.Draw(canvas)

    if ((stimulus_pos + home_run) <= len(data[:,0])) :
        for key, val in enumerate(iteree) :
            current         = moveToAxis(data[:,val][stimulus_pos:(stimulus_pos + home_run)])
            suspectedMax    = max(current[first_base:home_run])
            averageBefore   = np.average(current[first_base:home_run])
            percentageDiff  = countPercentageDifferent(suspectedMax, averageBefore)

            if (percentageDiff > 200) :
                fill_value  = (0,255,0)
            elif (percentageDiff > 100) :
                green_value = int(math.ceil((percentageDiff - 100) * 2)) + 55
                fill_value  = (0,green_value,0)
            else :
                red_value   = int(math.ceil((100 - percentageDiff) * 2)) + 55
                fill_value  = (red_value,0,0)
            if (percentageDiff < 99) :
                text_pos    = (position[key][0] - (radius * 0.6), position[key][1] - (radius * 0.6))
            else :
                text_pos    = (position[key][0] - (radius * 0.9), position[key][1] - (radius * 0.6))

            addition.ellipse((position[key][0] - (radius + outline), position[key][1] - (radius + outline), position[key][0] + (radius + outline), position[key][1] + (radius + outline)), fill=line_color)
            addition.ellipse((position[key][0] - radius, position[key][1] - radius, position[key][0] + radius, position[key][1] + radius), fill=fill_value)
            addition.text(text_pos, str(int(math.ceil(percentageDiff))), font=font, fill=text_color)

        del addition

        saveImage(canvas, direction)

def run() :
    start_time      = time.time()

    files           = findFiles(folders, grouped_val)
    randomed        = randomPick(files, files_amn, grouped_val)

    for filepath in randomed :
        data        = readFromFile(filepath)
        timestamp   = data[:,0]

        stimuli     = loadStimuli(filepath)
        stimuli_ran = randomStimulus(stimuli, stimuli_amn, grouped_val)
        stimuli_pos = findStimulus(timestamp, stimuli_ran['time'])

        for stimulus_idx, stimulus_pos in enumerate(stimuli_pos) :
            iteree      = range(2, 16)

            canvas      = Image.open(imagepath)
            putChannel(canvas, data, stimulus_pos, iteree, stimuli_ran['direction'][stimulus_idx])

    elapsed_time    = time.time() - start_time
    print 'elapsed = %.3f s' % (elapsed_time)

if __name__ == "__main__":
    run()
    # print env_serial\
