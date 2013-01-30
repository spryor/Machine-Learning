#Author: Stephen Pryor
#Date: September 23, 2012

"""
Usage:
> python kmeans.py
  - defaults to 3 clusters and kmeans++ initialization
or
> python kmeans.py <k>
  - where <k> is the number of clusters you want to find
  - defaults to kmeans++ initialization
or
> python kmeans.py <k> <initialization>
  - where <k> is the number of clusters you want to find
  - where <initialization> is either "random" or "kmeans++" (not including the quotes)
"""

import matplotlib.pyplot as plt
from kmeans import *
from kmeans_util import *
import random
import sys

#-----------------------------------------------------------------------START - Get command line arguments
k = 3
initialization = "kmeans++"
if len(sys.argv) > 1:
  k = int(sys.argv[1])
if len(sys.argv) > 2:
  initialization = sys.argv[2].lower()
#-----------------------------------------------------------------------END - Get command line arguments

model = kmean(k, 2)

#-----------------------------------------------------------------------START - Creat a test set
testData = getClickData()
#-----------------------------------------------------------------------END - Creat a test set

#-----------------------------------------------------------------------START - Train the model
sys.stdout.write("Training the model...")
if initialization == "canopy":
  initial_centroids = model.train_canopyClustering(testData, float(sys.argv[3]), float(sys.argv[4]))
elif initialization == "kmeans++_canopy":
  initial_centroids = model.train(testData, "kmeans++canopy")
else:
  initial_centroids = model.train(testData, initialization)
print "complete!"
#-----------------------------------------------------------------------START - Train the model

#-----------------------------------------------------------------------START - Cluster the test data
sys.stdout.write("Generating clusters...")
clusters = model.cluster(testData)
print "complete!"
#-----------------------------------------------------------------------END - Cluster the test data

#-----------------------------------------------------------------------START - Generate Plots
colors = ['m', 'b', 'g', 'r', 'c', 'y', 'k']
colorIndex = 0
for i in range(model.K):
  x, y = getX_Y(clusters[i])
  plt.plot(x, y, colors[colorIndex]+'o')
  colorIndex = colorIndex + 1
  if colorIndex >= len(colors):
    colorIndex = 0
    
c_x, c_y = getX_Y(initial_centroids)
fc_x, fc_y = getX_Y(model.centroids)
plt.plot(c_x, c_y, 'cs', label='Initial centroids')
plt.plot(fc_x, fc_y, 'rs', label='Final centroids')
plt.legend(loc='upper right')
plt.title('Clustered Data')
plt.ioff()
plt.show()
#-----------------------------------------------------------------------END - Generate Plots
