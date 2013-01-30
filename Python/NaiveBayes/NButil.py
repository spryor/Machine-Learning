#Author: Stephen Pryor
#Date: 5/13/12

import re
import os

_re_html = re.compile("<.*?>")
_re_nonAlphaNumericCharacters = re.compile("[^A-Za-z0-9_ ]")
_re_numbers = re.compile("(\s+|^)[0-9]+(\s+|$)")
_re_whiteSpace = re.compile("\s+")
stopWords = "(you|me|but|there|ive|from|had|then|to|his|is|her|he|she|shall|would|could|would|over|find|its|at|down|up|what|and|much|more|do|not|too|we|has|by|played|play|all|can|have|been|oh|dont|think|they|if|of|the|in|to|be|is|a|on|it|for|with|an|are|was|this|movie|film|as|i|that)"
_re_stopWords = re.compile("(\s+|^)"+stopWords+"(\s+|$)")

#a function to tokenize a string of words
def tokenize(contents):
  return contents.split(" ")

#function to clean up a string so there are
#no html tags, non alpha numeric characters
#single numbers, or sequences of whitespace
def cleanFile(contents):
  contents = contents.lower()
  contents = _re_html.sub(" ", contents)
  contents = _re_nonAlphaNumericCharacters.sub("", contents)
  contents = _re_numbers.sub(" <number> ", contents)
  contents = _re_numbers.sub(" <number> ", contents)
  #contents = _re_stopWords.sub(" ", _re_stopWords.sub(" ", contents))
  contents = _re_whiteSpace.sub(" ", contents)
  return contents.strip()

#a function to read in a file and return it as a string
def getFileAsString(filePath):
  openedFile = open(filePath)
  output = ""
  for line in openedFile:
    output = output + line
  openedFile.close()
  return output

#a function to extract a feature vector from a tokenized document
#in this case, a feature is a single word

def getFeatureVector(document, n=3):
  featureVector = {}
  features = (" ".join(document[i:i+n]) for i in range(len(document)-n+1))
  for feature in features:
    try:
      featureVector[feature] = featureVector[feature] + 1
    except:
      featureVector[feature] = 1
  return featureVector

#a function to open training files
#the first argument is a the maximum files to open for every class
#afterwards is an arbitrary number of directories with files you want to open
#each directory is associated with a class
#Usage example:
#dataset = getDataSet(200, POS="positiveDocuments/", NEG="negativeDocuments/")
#or
#dataset = getDataSet(200, POS="positiveDocuments/", NEG="negativeDocuments/", n=2) 
def getDataSet(maxNumDocs, **kwargs):
  n=3 #default features are trigrams
  try: 
    n = kwargs["n"]
    del kwargs["n"]
  except: pass 
  D = {}
  for key in kwargs:
    D[key] = []
    numDocs = 0
    listing = os.listdir(kwargs[key])
    for filePath in listing:
      if numDocs == maxNumDocs:
        break
      D[key].append(getFeatureVector(tokenize(cleanFile(getFileAsString(kwargs[key]+filePath))), n))
      numDocs = numDocs + 1
  return D