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
  
  #The Kmeans++ algorithm for initializing the cluster centroids
  #Implemented based on http://ilpubs.stanford.edu:8090/778/1/2006-13.pdf
  def init_kmeans_plusplus_canopy(self, D, radius):
    centroids = []
    data = copy.deepcopy(D)
    while len(centroids) < self.K:
      sum = 0.0
      distances = {}
      for point in data:
        point = tuple(point)
        distances[point] = min([999999999.9]+[self.similarity(point, center) for center in centroids])
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
            data = [p for p in data if self.similarity(p, list(point)) > radius]
            break
      #x, y = getX_Y(data)
      #plt.ioff()
      #plt.plot(x, y, 'go')
      #plt.show()
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
        elif init == "kmeans++canopy":
          self.centroids = self.init_kmeans_plusplus_canopy(D, 50)
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
  
  #trains the model using canopy clustering initialization, e.g. finds the centroids
  def train_canopyClustering(self, D, t1, t2):
    if not t1 >= t2:
      print "Error: t1 >= t2 property is not satisfied"
      exit()
    restart = True
    initial_centroids = []
    while restart:
      try:
        restart = False
        #START - Find canopies
        data = copy.deepcopy(D)
        canopies = []
        canopy_assignments = {}
        canopy_count = 0
        while len(data) > 0:
          currentCenter_index = random.randrange(0, len(data))
          currentCenter = data[currentCenter_index]
          canopies.append(currentCenter)
          tmpData = []
          for point in data:
            dist = self.similarity(point, currentCenter)
            if dist < t1:
              try:
                canopy_assignments[tuple(point)].append(canopy_count)
              except:
                canopy_assignments[tuple(point)] = [canopy_count]
            if not dist < t2:
              tmpData.append(point)
          data = tmpData
          canopy_count = canopy_count + 1
        plot.ioff()
        fc_x, fc_y = getX_Y(D)
        plot.plot(fc_x, fc_y, 'bo')
        fc_x, fc_y = getX_Y(canopies)
        plot.plot(fc_x, fc_y, 'cs')
        plot.show()
        #END - Find canopies
        #self.centroids = self.init_random(canopies)
        if len(canopies) >= self.K:
          self.centroids = self.init_kmeans_plusplus(canopies)
        else:
          self.centroids = self.init_kmeans_plusplus(D)
        initial_centroids = copy.deepcopy(self.centroids)
        #compute initial assignments
        a = [-1 for i in range(len(D))]
        converged = False
        numIter = 0
        while not converged and numIter < self.maxIter:
          numIter = numIter + 1
          converged = True
          for i in range(len(D)):
            changed = False
            dists = [float("inf") for k in range(self.K)]
            for k in range(self.K):
              i_asgn = canopy_assignments[tuple(D[i])]
              k_asgn = canopy_assignments[tuple(self.centroids[k])]
              if len(set(i_asgn).intersection(set(k_asgn))) > 0:
                dists[k] = self.similarity(self.centroids[k], D[i])
                changed = True
            if changed:
              assignment = self.argmin(dists)
              #print `dists`+" -> "+ `assignment`
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
    