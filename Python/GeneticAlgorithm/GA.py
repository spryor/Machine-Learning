#Author: Stephen Pryor
#Date: May 19, 2012

import matplotlib.pyplot as plt
from GA_util import *
import random
import math
import copy
import sys

numItemsToSort = 16 #the number of inputs to be sorted
sizeSortNetwork = 100 #the maximim allowed sort network in the initial population
sizePopulation = 100 #the size of the sorting network population
percentWinners = .1 #the number of 
chanceOfMutation = .3 #the probability of a mutation
amountOfMutation = .2 #how much to mutate a network if mutation occurs
k = 50 #save the top k best sorting networks directly
topToSave = int(percentWinners*sizePopulation) #the number of top sorting networks to use for mutation and crossover
sizeInputs = 50 #the size of the input population
topToSaveInputs = int(.2*sizeInputs) 
numIters = 2000 #the maximium number of iterations
population = []

#-----------------------------------------------------------------------START - Initialize a population of inputs
sys.stdout.write("Generating population of " + `sizeInputs` + " inputs...")
inputs = [[j+1 for j in shuffleList(range(numItemsToSort))] for i in range(sizeInputs)]
print "complete!"
#-----------------------------------------------------------------------END - Initialize a population of inputs

#-----------------------------------------------------------------------START - Initialize a population of random sort networks
sys.stdout.write("Generating population of " + `sizePopulation` + " sort networks...")
population = [createSortNetwork(sizeSortNetwork, numItemsToSort) for i in range(sizePopulation)]
print "complete!"
#-----------------------------------------------------------------------END - Initialize a population of random sort networks

#-----------------------------------------------------------------------START - Perform learning

iterAvgScore = [] # list to store avg score per generation statistics
iterAvgNetLength = [] # list to store avg network length per generation statistics

print "Starting learning..."
for iteration in range(numIters):
  scoreList = []
  #score the networks
  maxNetworkLength = max([len(network) for network in population])
  evaluationInputs = random.sample(inputs, 20)
  fitnessList = [(getAverageFitness(copy.deepcopy(evaluationInputs), network, maxNetworkLength), network) for network in population]
  #normalize the probabilities
  sumFitness = 0.0
  for (score, network) in fitnessList:
    sumFitness = sumFitness + score
  fitnessList = [(score/sumFitness, network) for (score, network) in fitnessList]
  fitnessList.sort()
  fitnessList.reverse()
  #select new population
  tmppopulation = []
  newpopulation = []
  #save the top k networks
  for i in range(k):
    newpopulation.append(fitnessList[i][1])
  #fill the rest of the new population
  while len(tmppopulation) < topToSave:
    for (score, network) in fitnessList:
      if random.random() <= score:
        tmppopulation.append(network)
  while len(newpopulation) < sizePopulation:
    if random.random() < chanceOfMutation:
      newpopulation.append(mutate(tmppopulation[random.randrange(0, topToSave)], amountOfMutation, numItemsToSort))
    else:
      ind1 = random.randrange(0, topToSave)
      ind2 = random.randrange(0, topToSave)
      for newInd in crossover(tmppopulation[ind1], tmppopulation[ind2]):
        newpopulation.append(newInd)
  population = newpopulation
  #get the statistics for the new population
  maxNetworkLength = max([len(network) for network in population])
  fitnessList = [(getAverageFitness(evaluationInputs, network, maxNetworkLength), network) for network in population]
  sumFitness = float(sum([score for (score, network) in fitnessList]))
  sumLengths = float(sum([len(network) for (score, network) in fitnessList]))
  avgScore = float(sumFitness)/float(len(fitnessList))
  avgLength = float(sumLengths)/float(len(fitnessList))
  iterAvgScore.append(avgScore)
  iterAvgNetLength.append(avgLength)
  print "\tIteration: "+`iteration`+"\tAvg Score: " + `avgScore` + "\tAvg NetworkLength: " + `avgLength`
  
  #The following can be included to coevolve the inputs to force the networks to solve
  #more inputs
  """
  #evolve inputs
  inputList = [(sum([getAverageFitness([copy.deepcopy(inp)], network, maxNetworkLength) for network in population]), inp) for inp in inputs]
  sumFit = float(sum([score for (score, inp) in inputList]))
  inputList = [(1.0-score/sumFit, inp) for (score, inp) in inputList]
  inputList.sort()
  inputList.reverse()
  tmpinputs = []
  newinputs = []
  for i in range(5):
    newinputs.append(inputList[i][1])
  while len(tmpinputs) < topToSaveInputs:
    for (score, inp) in inputList:
      if random.random() <= score:
        tmpinputs.append(inp)
  while len(newinputs) < sizeInputs:
    if random.random() < chanceOfMutation:
      newinputs.append([j+1 for j in shuffleList(range(numItemsToSort))])
    else:
      ind1 = random.randrange(0, topToSaveInputs)
      ind2 = random.randrange(0, topToSaveInputs)
      for newInd in crossoverInput(tmpinputs[ind1], tmpinputs[ind2]):
        newinputs.append(newInd)
  inputs = newinputs
  """
#-----------------------------------------------------------------------END - Perform learning

print "...complete!"
plt.plot(range(len(iterAvgScore)), iterAvgScore, 'r-')
plt.title('Average Fitness Per Generation')
plt.show()
plt.plot(range(len(iterAvgNetLength)), iterAvgNetLength, 'b-')
plt.title('Average Network Length Per Generation')
plt.show()

#The following code will the save the iteration stats to a file
"""
f = open('results.csv', 'w')
for i in range(len(iterAvgScore)):
  f.write(`iterAvgScore[i]`+","+`iterAvgNetLength[i]`+"\n")
f.close()
"""
  

