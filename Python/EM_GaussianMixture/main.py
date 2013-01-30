#Author: Stephen Pryor
#Date: May 18, 2012

"""
Usage:
Running with no command line arguments will look for 3 clusters and not run in interactive mode
OR
>main.py <k>
  - where k is the number of clusters
OR
>main.py <k> show
  - where k is the number of clusters
  - show will display EM running in realtime
"""

from GMM import *
from GMM_util import *
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import sys

#the number of clusters to find
K = 3

interactiveMode = False
if len(sys.argv) > 1:
  K = int(sys.argv[1])
if len(sys.argv) > 2 and sys.argv[2] == "show":
  interactiveMode = True

#-----------------------------------------------------------------------START - Creat a test set
print "Creating a test set..."
X = getClickData()
print "...complete!"
#-----------------------------------------------------------------------END - Creat a test set

GM = GaussianMixtureModel(K, .0001) #create the model

#-----------------------------------------------------------------------START - Initialize the model
sys.stdout.write("Initializing the model...")
mu, sigma, mixCo, gammas = GM.randomInitialization(X)
print "complete!"
#-----------------------------------------------------------------------END - Initialize the model

colors = ['r', 'b', 'g', 'y', 'm', 'k']
plt.ion()
#-----------------------------------------------------------------------START - Display the initial clustering
sys.stdout.write("Displaying the clustering before EM...")
clusters = GM.cluster(X, mu, sigma)
plt.figure()                       
i = 0
for cluster in clusters: 
  x, y = getX_Y(cluster)
  plt.plot(x, y, colors[i]+'o')
  i = i + 1
  if i >= len(colors):
    i = 0
plt.title('Random Initialization')
print "complete!"
plt.draw()
#-----------------------------------------------------------------------END - Display the initial clustering

#-----------------------------------------------------------------------START - Train the model with EM
print "Running EM..."
if interactiveMode: #To run while updating the plot
  mu, sigma = GM.EM(X, mu, sigma, mixCo, gammas, plt, colors)
else:               #To run without updating the plot
  mu, sigma = GM.EM(X, mu, sigma, mixCo, gammas, False, False)
print "...complete!"
#-----------------------------------------------------------------------END - Train the model with EM

#-----------------------------------------------------------------------START - Display the post EM clustering
sys.stdout.write("Displaying the clustering after EM...")
clusters = GM.cluster(X, mu, sigma)
i = 0
for cluster in clusters: 
  x, y = getX_Y(cluster)
  plt.plot(x, y, colors[i]+'o')
  i = i + 1
  if i >= len(colors):
    i = 0
plt.title('Clustered Data')
print "complete!"
plt.ioff()
plt.show()
#-----------------------------------------------------------------------END - Display the post EM clustering

