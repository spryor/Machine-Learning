#Author: Stephen Pryor
#Date: 10/6/12

import matplotlib.pyplot as plt
import numpy as np
import math
import random
import sys

def genDataPoints(x, x_stdev, y, y_stdev, numDataPoints = 100):
  data = []
  for i in range(numDataPoints):
    data.append([random.gauss(x, x_stdev), random.gauss(y, y_stdev)])
  return data

def getX_Y(dataset):
  x = []
  y = []
  for vector in dataset:
    x.append(vector[0])
    y.append(vector[1])
  return x, y

data = []
def getClickData():    
  def onclick(event):
    global data, plt
    sys.stdout.write("\t\tAdded 50 points with a mean of ("+`event.xdata`+", "+`event.ydata`+")\n")
    data = data + genDataPoints(event.xdata, 14, event.ydata, 10, 50)
    x, y = getX_Y(data)
    plt.plot(x, y, 'ro')
    return event.xdata, event.ydata

  plt.ion()
  plt.figure()  
  plt.xlim([0,400])
  plt.ylim([0,400])
  plt.title('Click to add data')
  plt.connect('button_press_event', onclick)
  
  raw_input("\tPress enter when complete:\n\n ")
  plt.close()
  return np.matrix(data)