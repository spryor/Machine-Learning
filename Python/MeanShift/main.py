#Author: Stephen Pryor
#Date: 10/6/12

"""
Usage:
>main.py
  - clusters your provided data using a default bandwith of 56
>main.py <h>
  - clusters your provided data using a bandwith of <h>
NOTE: This code has not been optimized, so adding a lot of datapoints will be slow.
"""

import matplotlib.pyplot as plt
from mean_shift_util import *
from mean_shift import * 
import sys

#-----------------------------------------------------------------------START - Check for parameters
h = 50
if len(sys.argv) > 1:
  h = float(sys.argv[1])
#-----------------------------------------------------------------------END - Check for parameters

sys.stdout.write("Generating Dataset...")
originalData = getClickData() #get the data to cluster
print "complete!"

sys.stdout.write("Clustering Data...")
meanShift = mean_shift(h)
clusters = meanShift.cluster(originalData) #cluster the data
print "complete!"

#-----------------------------------------------------------------------START - Plot the results
sys.stdout.write("Displaying Results...")
for cluster in clusters:
  cluster = np.matrix(cluster)
  plt.plot(cluster[:, 0], cluster[:, 1], 'o')
plt.ioff()
plt.xlim([0,400])
plt.ylim([0,400])
plt.title(`len(clusters)`+" Clusters")
print "complete!"
plt.show()
#-----------------------------------------------------------------------END - Plot the results
