'''
Created by rahil vora 10/22/2016
'''
import os
import numpy as np

def readFile(filename):
    with open(filename,'r') as file:
        data = file.read()
        return data

documents = {}

def readFileIntoDict(filename1,filename2):
    doc = 1
    with open(filename1,'r') as file:
        for line in file:
            value = line
            documents[doc] = value
            doc += 1
    with open(filename2,'r') as file:
        for line in file:
            value = line
            documents[doc] = value
            doc += 1


def convertToVector(documents):
    for document in documents:
        temp = documents[document].split()
        createVector(temp)

vectorizedDocuments = []
def createVector(docList):
    doc = {}
    for i in range(0, len(docList), 2):
       doc[docList[i]] = docList[i+1]
    vectorizedDocuments.append(doc)

def calculateCosineSimilarity(doc1, doc2):
    dot_product = 0
    sum1 = 0
    sum2 = 0
    for key in doc1:
        if key in doc2:
            dot_product += int(doc1[key]) * int(doc2[key])
    for item in doc1:
        sum1 += int(doc1[item])**2

    for item in doc2:
        sum2 += int(doc2[item])**2

    print(dot_product/(np.sqrt(sum1)*np.sqrt(sum2)))
if __name__ == "__main__":
    wiki1File = os.path.join("data", "wiki1.csr")
    wiki2File = os.path.join("data", "wiki2.csr")
    readFileIntoDict(wiki1File, wiki2File)
    convertToVector(documents)
    print(len(vectorizedDocuments))
    calculateCosineSimilarity(vectorizedDocuments[0], vectorizedDocuments[2]);
    data1 = readFile(wiki1File)
    data2 = readFile(wiki2File)

