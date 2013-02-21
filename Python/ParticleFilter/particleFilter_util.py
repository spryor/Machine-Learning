#Author: Stephen Pryor
#Date: September 27, 12

import math

def getX_Y(dataset):
  x = []
  y = []
  for vector in dataset:
    x.append(vector[0])
    y.append(vector[1])
  return x, y

def euclidean_distance(v, u):
  return math.sqrt(sum([math.pow(v[i] - u[i], 2) for i in range(len(v))]))