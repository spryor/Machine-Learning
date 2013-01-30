#Author: Stephen Pryor
#Date: 10/6/12

"""
This is my implementation of the Mean Shift algorithm applied for Clustering.

Useful references which I used to help my understanding of the algorithm:
http://saravananthirumuruganathan.wordpress.com/2010/04/01/introduction-to-mean-shift-algorithm/
http://www.inf.tu-dresden.de/content/institutes/ki/is/VORTRAG/Vortrag_Huong_Nguyen.pdf
http://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/TUZEL1/MeanShift.pdf
http://www.cse.yorku.ca/~kosta/CompVis_Notes/mean_shift.pdf
"""

import numpy as np
import math
import copy

class mean_shift:
  def __init__(self, h):
    self.h = h #h is the bandwith parameters
  
  #The clustering algorithm
  #NOTE: Notice that I am calling the meanShift function twice (with an adjusted h).
  #      This is to help overcome some incorrect clustering for odd shapes.
  #      This also slows the algorithm down.
  def cluster(self, initialData):
    return self.assignClusters(initialData, self.meanShift(self.meanShift(initialData, self.h), 0.5*self.h))
  
  #The meanshift algorithm
  def meanShift(self, initialData, h):
    data = copy.deepcopy(initialData)
    for i in range(len(data)):
      difference = 99
      while difference > 0.0:
        x = data[i]
        numerator = 0.0
        denominator = 0.0
        for x_i in initialData:
          g = math.exp(-1.0*math.pow(np.linalg.norm((x - x_i)/h), 2))
          numerator = numerator + x_i*g
          denominator = denominator + g
        ms = numerator/denominator - x
        newPoint = x + ms
        data[i] = newPoint
        difference = np.linalg.norm(x-newPoint)
    return data
  
  #assign the datapoints to clusters
  def assignClusters(self, data, shiftedData):
    N, D = data.shape
    clusterCenter = []
    clusters = []
    for i in range(len(shiftedData)):
      currentCluster = -1
      for c in range(len(clusterCenter)):
        if np.linalg.norm(shiftedData[i]-clusterCenter[c]) < self.h:
          currentCluster = c
      if currentCluster > -1:
        clusterCenter[currentCluster] = shiftedData[i, :]
        clusters[currentCluster].append([data[i, j] for j in range(D)])
      else:
        clusterCenter.append(shiftedData[i,:])
        clusters.append([])
    return clusters
