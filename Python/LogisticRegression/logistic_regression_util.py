#Author: Stephen Pryor
#Date: 10/7/12

import numpy as np
import random
import math

def generateData(clusterSize):
  clusterOne = []
  for i in range(clusterSize):
    x = random.gauss(10, 10)
    clusterOne.append([0, 1, x, x+math.fabs(random.gauss(0, 20))])
  clusterTwo = []
  for i in range(clusterSize):
    x = random.gauss(10, 10)
    clusterTwo.append([1, 1, x, x-math.fabs(random.gauss(0, 20))])
  data = np.matrix(clusterOne+clusterTwo)
  return data, data[:,1:4], data[:,0]

def displayClassification(pyplot, model, X, data):
  for i in range(len(X)):
    pred_v = model.predict(X[i])
    if pred_v == 1:
      pyplot.plot((X[i])[0, 1], (X[i])[0, 2], 'gs')
      if pred_v != (data[i])[0, 0]:
        pyplot.plot((X[i])[0, 1], (X[i])[0, 2], 'ro')
    else:
      pyplot.plot((X[i])[0, 1], (X[i])[0, 2], 'b^')
      if pred_v != (data[i])[0, 0]:
        pyplot.plot((X[i])[0, 1], (X[i])[0, 2], 'ro')
  pyplot.title('Class Assignments: Errors are red')
  pyplot.show()