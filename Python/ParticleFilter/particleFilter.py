#Author: Stephen Pryor
#Date: September 27, 12
"""
This particle filter is implemented based off of page 98 in Probabilistic Robotics by Sebastian Thrun, et al.
"""
from particleFilter_util import *
import random
import math

def particle_filter(X, observations, objects, windowSize):
  W = [[] for i in range(len(objects))]
  max_W = [0.0 for i in range(len(objects))]
  for j in range(len(X)):
    for i in range(len(objects)):
      W[i].append(math.fabs(euclidean_distance(X[j], objects[i])-observations[i]))
      if W[i][j] > max_W[i]:
        max_W[i] = W[i][j]

  W_final = []
  for i in range(len(X)):
    prob = 1.0
    for j in range(len(objects)):
      prob = prob * (1.0-W[j][i]/max_W[j])
    W_final.append(prob)
  X_tmp = []
  j = 0
  for i in range(0, int(math.floor(len(X)*0.04))):
    X_tmp.append((random.randrange(0, windowSize), random.randrange(0, windowSize)))
  while len(X_tmp) < len(X):
    if random.random() < W_final[j]:
      point = (random.gauss(X[j][0], random.randrange(20, 30)), random.gauss(X[j][1], random.randrange(20, 30)))
      X_tmp.append(point)
    j = j + 1
    if j >= len(X):
      j = 0
  return X_tmp