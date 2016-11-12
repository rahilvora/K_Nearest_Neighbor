import sys, os, math
from collections import OrderedDict

allTermFrequencies = []
documentFrequency = {}
IDF = {}
cosineSimilaritiesDict = {}
epsilon = 0.0

def readFile(file):
    with open(file,'r') as file:
        for line in file:
            getTermFrequencyDict(line.split())


def getTermFrequencyDict(termAndFrequencies):
    termFrequenciesDict = {}
    noOfTerms = len(termAndFrequencies) / 2
    for i in range(0, len(termAndFrequencies), 2):
        termFrequenciesDict[termAndFrequencies[i]] = float(termAndFrequencies[i + 1]) / noOfTerms
        if (documentFrequency.has_key(termAndFrequencies[i])):
            documentFrequency[termAndFrequencies[i]] += 1
        else:
            documentFrequency[termAndFrequencies[i]] = 1
    allTermFrequencies.append(termFrequenciesDict)

def getIDFForAllTerms():
    for key in documentFrequency.keys():
        IDF[key] = 1.0 + math.log(len(allTermFrequencies) / documentFrequency[key])

def calculateCosineSimilarityForAPair(doc1, doc2, row, col):
    dot_product = 0
    sum1 = 0
    sum2 = 0
    for key in doc1:
        if key in doc2:
            dot_product += float(doc1[key]) * float(doc2[key])
    for item in doc1:
        sum1 += float(doc1[item]) ** 2

    for item in doc2:
        sum2 += float(doc2[item]) ** 2
    cosineSimilarity = dot_product / (math.sqrt(sum1) * math.sqrt(sum2))
    if cosineSimilarity < epsilon: return
    try:
        cosineSimilaritiesDict[row + 1].append((col+1, cosineSimilarity))
    except:
        cosineSimilaritiesDict[row + 1] = []
        cosineSimilaritiesDict[row + 1].append((col+1, cosineSimilarity))


def calculateCosineSimilarities():
    for i in range(0, len(allTermFrequencies)):
        for j in range(i + 1, len(allTermFrequencies)):
            calculateCosineSimilarityForAPair(allTermFrequencies[i], allTermFrequencies[j], i, j)
        cosineSimilaritiesDict[i + 1] = sortCosineSimilarities(cosineSimilaritiesDict[i + 1])

def sortCosineSimilarities(cosineSimilaritiest):
    return sorted(cosineSimilaritiest, key=lambda x: x[1], reverse = True)

# def calculateTFIDF():
#     for i in range(0, len(allTermFrequencies)):
#

if __name__ == "__main__":
    wiki1File = os.path.join("data", sys.argv[3])
    outputFile = os.path.join("data", sys.argv[4])
    epsilon = float(sys.argv[1])
    k = int(sys.argv[2])
    readFile(wiki1File)
    calculateCosineSimilarities()
