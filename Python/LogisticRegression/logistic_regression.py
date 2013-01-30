#Author: Stephen Pryor
#Date: 10/7/12

import numpy as np
import random
import math

class logistic_regression:
  def __init__(self):
    self._theta = 0.0
  
  def g(self, z):
    return 1.0/(1+math.exp(-z))
  
  def h(self, theta, x):
    return self.g(theta.T*x)
  
  def predict(self, x):
    if self.h(self._theta, x.T) >=.5:
      return 1
    else:
      return 0
  
  def J(self, theta, x, y):
    sum = 0.0
    m = len(x)
    for i in range(m):
      try:
        Y = (y[i])[0, 0]
        H = self.h(theta, x[i].T)
        sum = sum + Y*math.log(H)+(1-Y)*math.log(1.0-H)
      except: pass
    return -1*sum/float(m)
  
  def update(self, theta, x, y):
    for j in range(len(theta)):
      sum = 0.0
      m = len(x)
      for i in range(m):
        H = self.h(theta, x[i].T)
        sum = sum + (H-y[i])*(x[i])[:,j]
      sum = sum/float(m)
      theta[j,0] = theta[j,0] - sum
    return theta
    
  def train(self, X, Y):
    N, D = X.shape
    reset = True
    theta = np.matrix([[random.gauss(.5, 3)] for i in range(D)])
    attempts = 0
    while reset:
      reset = False
      try:
        j = self.J(theta, X, Y)
        prev_j = 999
        numIterations = 0
        maxIterations = 2000
        while math.fabs(j-prev_j) > 0.001 and maxIterations > numIterations:
          theta = self.update(theta, X, Y)
          prev_j = j
          j = self.J(theta, X, Y)
          numIterations = numIterations + 1
      except:
        attempts = attempts + 1
        if attempts > 20:
          print "Failed: Reset iterations limit of 20 reached"
          exit()
        reset = True
        theta = np.matrix([[random.gauss(.5, 3)] for i in range(D)])
    self._theta = theta