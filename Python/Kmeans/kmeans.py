#Author: Stephen Pryor
#Date: September 23, 2012
"""
The Kmeans clustering algorithm
"""
import matplotlib.pyplot as plot
from kmeans_util import *
import math
import random
import operator
import copy

class kmean:
  def __init__(self, k, vec_dim, maxIter=6000):
    self.K = k
    self.dim = vec_dim
    self.centroids = []
    self.maxIter = maxIter
  
  #returns the index of the largest element in a list
  def argmin(self, lst):
    return lst.index(min(lst))
  
  #multiplies a vector (a list) a by the constant c
  def multiplyVectorByConstant(self, a, c):
    for i in range(len(a)):
      a[i] = a[i]*c
  
  #adds the two vectors a and b (where a and b are list)   
  def addVectors(self, a, b):
    for i in range(len(a)):
      a[i] = a[i] + b[i]
  
  #returns the euclidian distance between v and u
  def similarity(self, v, u):
    distance = 0.0
    for i in range(len(v)):
      distance = distance + math.pow(v[i] - u[i], 2)
    return math.sqrt(distance) 
  
  #randomly initialize the centroids
  def init_random(self, D):
    return random.sample(D, self.K)
     
  #The Kmeans++ algorithm for initializing the cluster centroids
  #Implemented based on http://ilpubs.stanford.edu:8090/778/1/2006-13.pdf
  def init_kmeans_plusplus(self, D):
    centroids = random.sample(D, 1)
    while len(centroids) < self.K:
      sum = 0.0
      distances = {}
      for point in D:
        point = tuple(point)
        distances[point] = min([self.similarity(point, center) for center in centroids])
        sum = sum + distances[point]
      for point in distances:
        distances[point] = distances[point]/sum
      selected = False
      rn = random.random()
      while not selected:
        for point, prob in distances.items():
          if prob >= random.random():
            centroids.append(list(point))
            selected = True
            break
    return centroids
  
  #trains the model, e.g. finds the centroids
  def train(self, D, init="kmeans++"):
    restart = True
    initial_centroids = []
    while restart:
      try:
        restart = False
        if init == "random":
          self.centroids = self.init_random(D)
        elif init == "kmeans++":
          self.centroids = self.init_kmeans_plusplus(D)
        else:
          print "Error: "+`init`+" is not a recognized initialization"
        initial_centroids = copy.deepcopy(self.centroids)
        #compute initial assignments
        a = [-1 for i in range(len(D))]
        converged = False
        numIter = 0
        while not converged and numIter < self.maxIter:
          numIter = numIter + 1
          converged = True
          for i in range(len(D)):
            assignment = self.argmin([self.similarity(self.centroids[k], D[i]) for k in range(self.K)])
            if assignment != a[i]:
              a[i] = assignment
              converged = False
          if not converged:
            for k in range(self.K):
              mean = [0]*self.dim
              count = 0
              for i in range(len(D)):
                if a[i] == k:
                  self.addVectors(mean, D[i])
                  count = count + 1
              self.multiplyVectorByConstant(mean, 1.0/float(count))
              self.centroids[k] = mean
      except:
        pass
    return initial_centroids
  
  #returns the feature vectors in D in clusters    
  def cluster(self, D):
    clusters = []
    for i in range(self.K):
      clusters.append([])
    for v in D:
      clusters[self.argmin([self.similarity(self.centroids[k], v) for k in range(self.K)])].append(v)
    return clusters
    