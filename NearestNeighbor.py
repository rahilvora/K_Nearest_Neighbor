import sys, os, math
import time, argparse

allTermFrequencies = []
documentFrequency = {}
IDF = {}
cosineSimilaritiesDict = {}
epsilon = 0.0
similarDocsCount = 0

def readFile(file):
    with open(file,'r') as file:
        for line in file:
            getTermFrequencyDict(line.split())

sumOfSquareRoots = []
def getTermFrequencyDict(termAndFrequencies):
    termFrequenciesDict = {}
    noOfTerms = len(termAndFrequencies) / 2
    for i in range(0, len(termAndFrequencies), 2):
        normalizedTF = float(termAndFrequencies[i + 1]) / noOfTerms
        termFrequenciesDict[termAndFrequencies[i]] = normalizedTF
        if (documentFrequency.has_key(termAndFrequencies[i])):
            documentFrequency[termAndFrequencies[i]] += 1
        else:
            documentFrequency[termAndFrequencies[i]] = 1

    allTermFrequencies.append(termFrequenciesDict)

def getIDFForAllTerms():
    for key in documentFrequency.keys():
        IDF[key] = 1.0 + math.log(len(allTermFrequencies) / documentFrequency[key])

def calculateCosineSimilarityForAPair(doc1, doc2, row, col):
    global similarDocsCount
    dot_product = 0
    for key in doc1:
        if key in doc2:
            dot_product += float(doc1[key]) * float(doc2[key])
    cosineSimilarity = dot_product / (sumOfSquareRoots[row] * sumOfSquareRoots[col])
    if cosineSimilarity < epsilon: return
    try:
        cosineSimilaritiesDict[row + 1].append((col+1, cosineSimilarity))
    except:
        currentCosineSimilarity = []
        currentCosineSimilarity.append((col+1, cosineSimilarity))
        cosineSimilaritiesDict[row + 1] = currentCosineSimilarity
    similarDocsCount += 1

def calculateCosineSimilarities():
    for i in range(0, len(allTermFrequencies), 1):
        for j in range(0, len(allTermFrequencies),1):
            if i == j:
                continue
            elif i > j:
                if j + 1 in cosineSimilaritiesDict.keys():
                    someitem = [item for item in cosineSimilaritiesDict[j + 1] if item[0] == i + 1]
                    if len(someitem) == 0:
                        continue
                    try:
                        cosineSimilaritiesDict[i + 1].append((j + 1, someitem[0][1]))
                    except:
                        cosineSimilaritiesDict[i + 1] = []
                        cosineSimilaritiesDict[i + 1].append((j + 1, someitem[0][1]))
            else:
                calculateCosineSimilarityForAPair(allTermFrequencies[i], allTermFrequencies[j], i, j)
        if((i + 1) in cosineSimilaritiesDict.keys()):
            cosineSimilarityTemp = sortCosineSimilarities(cosineSimilaritiesDict[i + 1])
            if(len(cosineSimilarityTemp) > k):
                cosineSimilaritiesDict[i + 1] = cosineSimilarityTemp[:k]

def getTFIDF():
    for i in range(0, len(allTermFrequencies)):
        sumOfSquares = 0
        for term in allTermFrequencies[i].keys():
            allTermFrequencies[i][term] = allTermFrequencies[i][term]*IDF[term]
            sumOfSquares += allTermFrequencies[i][term] ** 2
        sumOfSquareRoots.append(math.sqrt(sumOfSquares))

def sortCosineSimilarities(cosineSimilaritiest):
    return sorted(cosineSimilaritiest, key=lambda x: x[1], reverse = True)

def saveToOutputFile(outputFile):
    outputStr = ""
    for key in cosineSimilaritiesDict.keys():
        for tuple in cosineSimilaritiesDict[key]:
            currentLine = str(key) + " ; " + str(tuple[0]) + " ; " + str(tuple[1]) + "\n"
            outputStr += currentLine

    with open(outputFile, 'w') as outfile:
        outfile.write(outputStr)

def argumerSetter():
    parse = argparse.ArgumentParser(description="required arguments")
    parse.add_argument('-eps',default=0.9, type=float)
    parse.add_argument('-k', default=10, type=int)
    parse.add_argument('inputFile', default='wiki1.csr', type=str)
    parse.add_argument('outputFile', default='output.ijv', type=str)
    return vars(parse.parse_args())

if __name__ == "__main__":
    args = argumerSetter()
    startTime = time.time()
    wiki1File = os.path.join("data", args['inputFile'])
    outputFile = os.path.join("data", args['outputFile'])
    epsilon = args['eps']
    k = args['k']
    readFile(wiki1File)
    getIDFForAllTerms()
    getTFIDF()
    startTime2 = time.time()
    calculateCosineSimilarities()
    print("--- %s seconds Cosine Similarity ---" % (time.time() - startTime2))
    saveToOutputFile(outputFile)
    print "Number of neighbors " + str(similarDocsCount*2)
    print("--- %s seconds ---" % (time.time() - startTime))
