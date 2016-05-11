import os, sys, math, random
import numpy as np

from PIL import Image, ImageFont, ImageDraw
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import *

header      = ["F3","FC5","AF3","F7","T7","P7","O1","O2","P8","T8","F8","AF4","FC6","F4"]

font        = ImageFont.truetype("FreeSans.ttf", 28)
filepath    = 'images/coalesce/base.jpg'
# base        = Image.open(filepath)

sourceList  = [
    'data/20160503/174424_p300_stop_20.csv',
    'data/20160503/175805_p300_forward_20.csv',
    'data/20160503/180853_p300_left_20.csv',
    'data/20160503/181835_p300_right_20.csv'
]
first_base  = 18
home_run    = 65
radius      = 26
outline     = 3
line_color  = (0,0,0)
text_color  = (255,255,255)

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

def readFromFile(filename) :
    with open(filename) as afile :
        result = []
        for line in afile :
            splittedLine    = line.split(',')
            result.append([float(splittedLine[0])] +  map(int, splittedLine[1::1]))

        return np.array(result)

def loadStimulus(diff=0)  :
    with open('data/stimulus_out.csv') as afile :
        result  = []
        for line in afile :
            result.append(float(line) - diff)

        return np.array(result)

def run(source):
    # source          = sourceList[0]
    direction       = source.split('_')[2]

    data            = readFromFile(source)
    timestamp       = data[:,0]

    stimulus_out    = loadStimulus(5.0)
    stimulus        = findStimulus(timestamp, stimulus_out)

    for idx, value in enumerate(stimulus) :
        iteree      = range(2, 16)

        canvas      = Image.open(filepath)
        addition    = ImageDraw.Draw(canvas)

        if ((value + home_run) <= len(data[:,0])) :
            for key, val in enumerate(iteree) :
                current         = moveToAxis(data[:,val][value:(value+home_run)])
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

                # if (percentageDiff > 255) :
                #     clr_value   = 255
                # else :
                #     clr_value   = (int)(math.ceil(percentageDiff))

                if (percentageDiff < 99) :
                    text_pos    = (position[key][0] - (radius * 0.6), position[key][1] - (radius * 0.6))
                else :
                    text_pos    = (position[key][0] - (radius * 0.9), position[key][1] - (radius * 0.6))

                addition.ellipse((position[key][0] - (radius + outline), position[key][1] - (radius + outline), position[key][0] + (radius + outline), position[key][1] + (radius + outline)), fill=line_color)
                addition.ellipse((position[key][0] - radius, position[key][1] - radius, position[key][0] + radius, position[key][1] + radius), fill=fill_value)
                addition.text(text_pos, str((int)(math.ceil(percentageDiff))), font=font, fill=text_color)

            del addition

            destination = "result/dump/" + direction + "_" + str(idx + 0) + ".jpg"

            if not os.path.exists(os.path.dirname(destination)):
                try:
                    os.makedirs(os.path.dirname(destination))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            canvas.save(destination, "JPEG", quality=100, optimize=True, progressive=True)

if __name__ == "__main__":
    for source in sourceList : run(source)
    # run()
