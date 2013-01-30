#Author: Stephen Pryor
#Date: May 18, 2012

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
  plt.plot(0, 0, 'ro')
  plt.plot(200, 200, 'ro')
  plt.title('Click to add data')
  plt.connect('button_press_event', onclick)
  
  raw_input("\tPress enter when complete:\n\n ")
  plt.close()
  return np.matrix(data)

# A function for computing the multivariate gaussion PDF
#this function came from here: http://code.activestate.com/recipes/577735-expectation-maximization/
def gausPDF(x, m, s):
  N, D = x.shape
  xmt = np.matrix(x-m).transpose()
  for i in xrange(len(s)):
      if s[i,i] <= sys.float_info[3]: # min float
          s[i,i] = sys.float_info[3]
  sinv = np.linalg.inv(s)
  xm = np.matrix(x-m)
  return (2.0*math.pi)**(-D/2.0)*(1.0/math.sqrt(np.linalg.det(s)))\
          *math.exp(-0.5*(xm*sinv*xmt))

#a simple function to generate a random dataset
def generateDataset():
  testData = genDataPoints(5, 10, 5, 10)
  testData = testData + genDataPoints(64, 11, 65, 14)
  testData = testData + genDataPoints(6, 8, 65, 14)
  return np.matrix(testData)

#a function to generate an m by n matrix of small random numbers
def randomMatrix(m, n):
  return np.matrix([[random.random()*.2 for p in range(n)] for k in range(m)])

#takes a dataset (a list) and returns a list of x and y values 
def getX_Y(dataset):
  x = []
  y = []
  for vector in dataset:
    x.append(vector[0])
    y.append(vector[1])
  return x, y