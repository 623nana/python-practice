from numpy import *
from os import listdir
import operator
import sys

# train = 'trainingDigits'
# test = 'testDigits'

train = sys.argv[1]
test = sys.argv[2]

def classify0(inX, dataSet, labels, k):
  dataSetSize = dataSet.shape[0]
  diffMat = tile(inX, (dataSetSize, 1)) - dataSet
  sqDiffMat = diffMat ** 2
  sqDistances = sqDiffMat.sum(axis = 1)
  distances = sqDistances ** 0.5
  sortedDistIndicies = distances.argsort()
  classCount={}
  for i in range(k):
    voteIlabel = labels[sortedDistIndicies[i]]
    classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
  sortedClassCount = sorted(classCount.items(),
                            key=operator.itemgetter(1), reverse=True)
  return sortedClassCount[0][0]

def img2vector(filename):
  returnVect = zeros((1, 1024))
  fr = open(filename)
  for i in range(32):
    lineStr = fr.readline()
    for j in range(32):
      returnVect[0, 32*i+j] = int(lineStr[j])
  return returnVect

def hwClassifier():
  hwLabels = []

  trainingFileList = listdir(train)
  m = len(trainingFileList)
  trainingMat = zeros((m, 1024))
  for i in range(m):
    fileNameStr = trainingFileList[i]
    fileStr = fileNameStr.split('.')[0]
    classNumStr = int(fileStr.split('_')[0])
    hwLabels.append(classNumStr)
    trainingMat[i, :] = img2vector(train + '/%s' % fileNameStr)
  dirs = listdir(test)
  for i in range(1, 21):
    cnt = 0
    for file in dirs:
      testData = img2vector(test + '/%s' % file)
      classifierResult = classify0(testData, trainingMat, hwLabels, i)
      if classifierResult != int(file[0]):
        cnt +=1
    rslt = cnt/len(dirs)*100
    print(int(rslt))

if __name__ == "__main__":
  hwClassifier()
