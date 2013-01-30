#Author: Stephen Pryor
#Date: May 18, 2012
"""
A Gaussian Mixture Model:
The implementation of the included EM algorithm comes from Pattern Recognition and Machine Learning by Christopher Bishop
"""
from GMM_util import *
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import sys

class GaussianMixtureModel:
  #the class constructor, k is the number of clusters and threshold 
  #the is the change in the model likelihood which will be used to 
  #define convergence
  def __init__(self, k, threshold):
    self.k = k
    self.threshold = threshold
  
  #initializes the model paramters such as the means and covariance matrices
  def randomInitialization(self, X):
    N, D = X.shape
    mu = []
    sigma = []
    mixCo = [random.random() for i in range(self.k)]
    sumMixCo = sum(mixCo)
    gammas = []
    for i in range(self.k):
      randVec = np.matrix([random.random() for p in range(D)])
      mu.append(randVec+np.mean(X.T))
      sigma.append(np.matrix(np.cov(np.transpose((random.random()+.5)*X))))
      mixCo[i] = mixCo[i]/sumMixCo
      gammas.append([random.random() for j in range(N)])
    return mu, sigma, mixCo, gammas
  
  #runs the EM algorithm for the gaussion mixture model
  #return the means and covariance matrices of the clusters
  def EM(self, X, mu, sigma, mixCo, gammas, plt, colors, thresh=False):
    #initialize any remaining parameters
    N, D = X.shape
    loglik_threshold = self.threshold
    if thresh:
      loglik_threshold = thresh
    L_prev = -99999999
    L = 99999
    numIterations = 0
    #----------------------------------------------------------------Iterate until convergence
    while math.fabs(L_prev - L) > loglik_threshold:
      numIterations = numIterations + 1
      L_prev = L
      N_k = []
      L = 0.0
      #----------------------------------------------------------------E-step
      for i in range(N):
        sum = 0.0
        for j in range(self.k):
          gammas[j][i] = mixCo[j]*gausPDF(X[i], mu[j], sigma[j])
          sum = sum + gammas[j][i]
        for j in range(self.k):
          gammas[j][i] = gammas[j][i]/sum
      #----------------------------------------------------------------M-Step
      for j in range(self.k):
        N_k.append(0.0)
        mu[j] = np.zeros((1, D))
        sigma[j] = np.zeros((D, D))
        for i in range(N):
          N_k[j] = N_k[j] + gammas[j][i]
          mu[j] = mu[j] + gammas[j][i]*X[i]
        mu[j] = mu[j]*(1.0/N_k[j])
        mixCo[j] = N_k[j]/float(N)
        for i in range(N):
          tmp = X[i]-mu[j]
          sigma[j] = sigma[j] + gammas[j][i]*np.transpose(tmp)*tmp
        sigma[j] = (sigma[j]*(1.0/N_k[j]))
      #----------------------------------------------------------------Re-evaluate log likelihood to check for convergence
      for i in range(N):
        sum = 0.0
        for j in range(self.k):
          sum = sum + mixCo[j]*gausPDF(X[i], mu[j], sigma[j])
        L = L + math.log(sum)
      print "\tLikelihood: "+`L`
      if plt != False and colors != False:
        clusters = self.cluster(X, mu, sigma)
        q = 0
        for cluster in clusters: 
          g, h = getX_Y(cluster)
          plt.plot(g, h, colors[q]+'o')
          q = q + 1
          if q >= len(colors):
            q = 0
        plt.title('Iteration: '+`numIterations`)
        plt.draw()
    return mu, sigma
  
  #A function to compute the cluster assignments
  #of some data. For simplicity, hard clusters 
  #assignments are assumed.
  def cluster(self, X, mu, sigma):
    clusters = [[] for i in range(self.k)]
    n, d = X.shape
    for j in range(n):
      assignment = 0
      prevVal = 0.0
      for i in range(self.k):
        val = gausPDF(X[j,:], mu[i], sigma[i])
        if prevVal < val:
          prevVal = val
          assignment = i
        clusters[assignment].append([X[j, v] for v in range(d)])
    return clusters
    