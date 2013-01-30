#Author: Stephen Pryor
#Date: September 22, 2012

import math

def linearRegression(X, Y):
  XY=[X[i]*Y[i] for i in range(len(X))]
  XX=[x*x for x in X]
  
  sigmaX = sum(X)
  sigmaY = sum(Y)
  sigmaXY = sum(XY)
  sigmaXX = sum(XX)
  
  N=float(len(X))
  slope = (N*sigmaXY-(sigmaX*sigmaY))/(N*sigmaXX-sigmaX*sigmaX)
  intercept = (sigmaY-slope*sigmaX)/N
  
  return intercept, slope