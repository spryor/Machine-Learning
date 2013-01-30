#Author: Stephen Pryor
#Date: 10/7/12

#Note: At some point I'm going to clean this code up.
#      Right now it still needs to be vectorized.

import matplotlib.pyplot as plt
from logistic_regression import *
from logistic_regression_util import *
import numpy as np
import random
import math
import sys

#-----------------------------------------------------------------------START - Generating Dataset
sys.stdout.write("Generating dataset...")
data, X, Y = generateData(200)
print "complete!"
#-----------------------------------------------------------------------END - Generating Dataset

#-----------------------------------------------------------------------START - Train Model
sys.stdout.write("Training model...")
model = logistic_regression()
model.train(X, Y)
print "complete!"
#-----------------------------------------------------------------------END - Train Model

#-----------------------------------------------------------------------START - Plot the results
sys.stdout.write("Displaying classification results...")
displayClassification(plt, model, X, data)
print "complete!"
#-----------------------------------------------------------------------END - Plot the results
