#Author: Stephen Pryor
#Date: May 19, 2012

import random
import copy

#removeDuplicates 
def removeDuplicates(network):
  prev = -1
  duplicates = 0
  newNetwork = []
  for pair in network:
    if prev != -1 and prev != pair:
      newNetwork.append(pair)
    elif prev == -1:
      newNetwork.append(pair)
    prev = pair
  return newNetwork
  
#function to get a pairing for the sort network
def getSortTuple(numItemsToSort):
  randSelection = random.randrange(0, numItemsToSort)
  tmpSortList = [i for i in range(0,randSelection)+range(randSelection+1,numItemsToSort)]
  return (randSelection, random.choice(tmpSortList))

#create and return a random sorting network
def createSortNetwork(maxSortNetwork, numItemsToSort):
  network = []
  for i in range(random.randrange(1, maxSortNetwork)):
    network.append(getSortTuple(numItemsToSort))
  return removeDuplicates(network)

#sort a list using a sorting network
def sortL(lst, network):
  lst = copy.deepcopy(lst)
  for pair in network:
    largestIndex = pair[0]
    smallestIndex = pair[1]
    if largestIndex < smallestIndex:
      smallestIndex = largestIndex
      largestIndex = pair[1]
    if lst[smallestIndex] > lst[largestIndex]:
      tmp = lst[largestIndex]
      lst[largestIndex] = lst[smallestIndex]
      lst[smallestIndex] = tmp
  return lst

#perform a crossover between two networks using the "cut and splice" method
def crossover(networkOne, networkTwo):
  splitIndex1 = random.randrange(0, len(networkOne))
  splitIndex2 = random.randrange(0, len(networkTwo))
  return removeDuplicates(networkOne[:splitIndex1]+networkTwo[splitIndex2:]), removeDuplicates(networkTwo[:splitIndex2]+networkOne[splitIndex1:])

#perform a crossover between two networks
def crossoverInput(inp1, inp2):
  splitIndex = random.randrange(0, len(inp1))
  return inp1[:splitIndex]+inp2[splitIndex:], inp2[:splitIndex]+inp1[splitIndex:]

#mutate
def mutate(network, percentMutation, numItemsToSort):
  tempNetwork = copy.deepcopy(network)
  for i in range(len(tempNetwork)):
    if random.random() < percentMutation:
      if random.random() < 0.04:#0.05:
        tempNetwork.insert(i,getSortTuple(numItemsToSort))
      else:
        tempNetwork[i] = getSortTuple(numItemsToSort)
  return removeDuplicates(tempNetwork)

#function to return a score for how well a list is sorted
def sortScore(lst):
  sortBigrams = 0.0
  numBigrams = len(lst)-2
  for i in range(numBigrams):
    if lst[i] <= lst[i+1] and lst[i+1] <= lst[i+2]:
      sortBigrams = sortBigrams + 1.0
  return (sortBigrams/float(numBigrams))

#fitness function normalizing for network size
def fitness(lst, network, maxNetworkLength):
  sortW = .99999
  lengthW = 1.0 - sortW
  return sortW*sortScore(lst) + lengthW*(1.0-float(len(network))/float(maxNetworkLength))

#returns the average fitness of a subset of inputs
def getAverageFitness(subset, network, maxNetworkLength):
  averageNum = 0
  for lst in subset:
    averageNum = averageNum + fitness(sortL(lst, network), network, maxNetworkLength)
  return averageNum/float(len(subset))

#returns a shuffled list
def shuffleList(lst):
  random.shuffle(lst)
  return lst