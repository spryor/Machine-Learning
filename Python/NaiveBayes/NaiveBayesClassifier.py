#Author: Stephen Pryor
#Date: 5/13/12
"""
A Naive Bayes Classifier
"""
import math

class NaiveBayesClassifier:
  def __init__(self, alpha):
    self.classCounts = {}
    self.featureCounts = {}
    self.V_size = 0.0
    self.numFeaturesInClass = {}
    self.alpha = alpha
    self.totalNumDocuments = 0.0

  def train(self, D):
    uniqueFeatures = {}
    for label in D.keys():
      self.classCounts[label] = len(D[label])
      self.featureCounts[label] = {}
      self.numFeaturesInClass[label] = 0
      for featureVector in D[label]:
        for feature in featureVector.keys():
          try:
            self.featureCounts[label][feature] = self.featureCounts[label][feature] + featureVector[feature]
          except: 
            self.featureCounts[label][feature] = featureVector[feature]
          self.numFeaturesInClass[label] = self.numFeaturesInClass[label] + featureVector[feature]
          uniqueFeatures[feature] = 0
    self.V_size = float(len(uniqueFeatures.keys()))
    self.totalNumDocuments = float(sum([self.classCounts[label] for label in self.classCounts.keys()]))
  
  def probFeature(self, feature, label, denominator):
    featureCount = 0
    try:
      featureCount = self.featureCounts[label][feature]
    except:
      pass
    return math.log((float(featureCount) + self.alpha)/denominator, 2)
  
  def classify(self, featureVector):
    P_c = {}
    for label in self.classCounts.keys():
      P_c[label] = math.log(float(self.classCounts[label])/self.totalNumDocuments, 2)
      P_dc = 1.0
      denominator = (self.numFeaturesInClass[label]+self.alpha*(self.V_size))
      for feature in featureVector:
        P_dc = P_dc + -1*featureVector[feature]*math.fabs(self.probFeature(feature, label, denominator))
      P_c[label] = P_c[label] + P_dc
    return max(P_c, key=P_c.get)

      