#Author: Stephen Pryor
#Date: 5/13/12

#Uses the dataset found at http://ai.stanford.edu/~amaas/data/sentiment/index.html

import sys
from NaiveBayesClassifier import *
from NButil import *
import operator

#-----------------------------------------------------------------------START - Default Parameters
unigram = 1
bigram = 2
trigram = 3

numDocuments = 1000
gram = trigram
#-----------------------------------------------------------------------END - Default Parameters

#-----------------------------------------------------------------------START - Check for command line arguments
if len(sys.argv) > 1:
  numDocuments = int(sys.argv[1]) #the number of documents to use for training, -1 will use all available documents
  if len(sys.argv) > 2:
    if sys.argv[2] == "unigram":
       gram = unigram
    elif sys.argv[2] == "bigram":
       gram = bigram
    elif sys.argv[2] == "trigram":
       gram = trigram
#-----------------------------------------------------------------------END - Check for command line arguments

#-----------------------------------------------------------------------START - Load the training set
sys.stdout.write("Loading training set...")
trainingDataset = getDataSet(numDocuments, POS="sent/train/pos/", NEG="sent/train/neg/", n=gram)
print "complete!"
#-----------------------------------------------------------------------END - Load the training set

#-----------------------------------------------------------------------START - Create the NaiveBayesClassifier
classifier = NaiveBayesClassifier(1)
#-----------------------------------------------------------------------END - Create the NaiveBayesClassifier

#-----------------------------------------------------------------------START - Train the classifier
sys.stdout.write("Training classifier...")
classifier.train(trainingDataset)
print "complete!"

del trainingDataset
#-----------------------------------------------------------------------END - Train the classifier

#-----------------------------------------------------------------------START - Load the testing set
sys.stdout.write("Loading test set...")
testingDataset = getDataSet(numDocuments, POS="sent/test/pos/", NEG="sent/test/neg/", n=gram)
print "complete!"
#-----------------------------------------------------------------------END - Load the testing set

#-----------------------------------------------------------------------START - Evaulate the classifier
sys.stdout.write("Evaluating classifier...")
numCorrect = 0
numTotal = 0
for label in testingDataset.keys():
  for document in testingDataset[label]:
    results = classifier.classify(document)
    if label == results:
      numCorrect = numCorrect + 1
    numTotal = numTotal + 1
score = float(numCorrect)/float(numTotal)
print `score * 100.0`+"% accuracy"
#-----------------------------------------------------------------------END - Evaulate the classifier
