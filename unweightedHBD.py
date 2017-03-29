import math
from itertools import groupby
import collections
import numpy as np
import matplotlib.pyplot as plt
import itertools 
import pylab as pl
from matplotlib import collections  as mc
import sys

#name ='chicago'
#f = open(name+'A.txt')
#fcontents = f.read()
fcontents = sys.stdin.read()
def split_line(text):
    # split the text
    words = text.split()
    answer = [] 
    # for each word in the line:
    for word in words:
        # print the word
        answer.append(word)
    return answer

def coerce_int(text):
    answer= []
    for word in text:
        answer.append(int(word))
    return answer

edge = coerce_int(split_line(fcontents)) # an integer array of length 2*e of edge information, 1-start
n = max(edge)
e = int(len(edge)/2)
for i in range(len(edge)):
    edge[i] -= 1
# now edge is 0-start. It will remain this way.

class Edge(object):
#    def method_a(self, foo):
#        print (self.x + ' ' + foo)
    def __init__(self): 
        self.x = "hello" # can delete
        self.invertex = -1
        self.outvertex = -1
        self.edgeWeight = -1
        self.edgePQ = -1


class Vertex(object):
    def __init__(self):
        self.degree = -1
        self.rep = -1 # with the next segment, the rep will just be itself at the beginning
        self.componentSize = 0 # will update later
        self.death = -1
        self.index = -1 # the index is itself. We might not need to use this ever. Could delete, if not needed
        self.merge = -1 # in the end, merge == -1 if either the vertex is the main branch, or if it got merged along as a byproduct of another vertex merging 
        self.branchSize = [1] # will update later
        self.branchTime = [-1]
        self.mergeTime = -1 # TODO fill in below. Mark this the weight of the weidge when it's first merged
        self.uniqueBranchTime = []
        self.uniqueBranchSize = []
    def equal(self,v):
        if v.index == self.index:
            return True
        return False

arrV  = [Vertex() for i in range(n)]
for i in range(n):
    arrV[i].rep = i
    arrV[i].index = i


arrE  =[Edge() for i in range(e)]
for i in range(int(len(edge)/2)):
    if edge[2*i] < edge[2*i+1]:
        arrE[i].invertex = edge[2*i]
        arrE[i].outvertex = edge[2*i+1]
    else:
        arrE[i].invertex = edge[2*i+1]
        arrE[i].outvertex = edge[2*i]


tmp1 = []
tmp2 = []
for i in range(int(len(edge)/2)-1):
    if edge[2*i] < edge[2*i+1]:
        tmp1.append(edge[2*i])
        tmp2.append(edge[2*i+1])
    else:
        tmp2.append(edge[2*i])
        tmp1.append(edge[2*i+1])

adjMatrix = [[0 for i in range(n)] for j in range(n)]
for i in range(int(len(edge)/2)):
    if edge[2*i] < edge[2*i+1]:
        adjMatrix[edge[2*i]][edge[2*i+1]] +=1
    else:
        adjMatrix[edge[2*i+1]][edge[2*i]] +=1
uniqueEdge=[]
for i in range(n):
    for j in range(n):
        if adjMatrix[i][j] != 0:
            uniqueEdge.append(i)
            uniqueEdge.append(j)

edge = uniqueEdge
e = int(len(edge)/2)
arrE  =[Edge() for i in range(e)]
for i in range(int(len(edge)/2)):
    if edge[2*i] < edge[2*i+1]:
        arrE[i].invertex = edge[2*i]
        arrE[i].outvertex = edge[2*i+1]
    else:
        arrE[i].invertex = edge[2*i+1]
        arrE[i].outvertex = edge[2*i]

degreeCounter  = collections.Counter(uniqueEdge) # be CAREFUL. Here I use uniqueEdge. Don't need to if dne non-unique edges
for i in range(n):
    arrV[i].degree = degreeCounter.get(i)
    arrV[i].branchTime[0] = arrV[i].degree
for i in range(e):
    arrE[i].edgeWeight = min(arrV[arrE[i].invertex].degree,arrV[arrE[i].outvertex].degree )


arrEdgeWeight = []
for i in range(e):
    arrEdgeWeight.append(arrE[i].edgeWeight)

arrEdgePQ = sorted(range(len(arrEdgeWeight)), key=lambda k:arrEdgeWeight[k])
for i in range(e):
    arrE[arrEdgePQ[i]].edgePQ = e-1-i #0-start

arrEdgePQ = [0]*e
for i in range(e):
    arrEdgePQ[arrE[i].edgePQ] = i

def get_last(a):
    return a[len(a)-1]
def get(a,t): # specific for the usage below
    if t == len(a):
        return -2;
    else: return a[t]

# disjoint-set union-find, comparing rep's degree. Merge to the larger degreed rep.
for k in range(e):
    i = arrEdgePQ[k]
    currE = arrE[i] # edges are stored in an array of edges, called arrE. This is an index.
    w=currE.outvertex # index of the out-vertex
    v= currE.invertex # index of the in-vertex
    repV = arrV[v].rep # vertices are stored in an array of vertices, called arrV. This is an index.
    repW = arrV[w].rep # This is an index.
    if arrV[v].rep != arrV[w].rep: 
        branchCounter = 0
        
        if arrV[repV].degree >= arrV[repW].degree: # union by degree
            #print(str(repW) + ' '+str(w) + ' '+ str(v))
            if arrV[w].mergeTime == -1:
                arrV[w].mergeTime = currE.edgeWeight
            if arrV[repW].mergeTime == -1:
                arrV[repW].mergeTime = currE.edgeWeight
            for j in range(n):
                if arrV[j].rep == repW:
                    arrV[j].rep = repV
                    if arrV[j].death == -1: # update vertex death time
                        arrV[j].death = arrE[i].edgeWeight
                        arrV[j].merge = repV
                    elif currE.edgeWeight == arrV[j].mergeTime:
                        arrV[j].merge = repV
            branchCounter += get_last(arrV[repW].branchSize)
            arrV[repW].branchSize.append(0)
            arrV[repV].branchSize.append(get_last(arrV[repV].branchSize) + branchCounter)
            arrV[repV].branchTime.append(currE.edgeWeight)
            arrV[repW].branchTime.append(currE.edgeWeight)
            
        else: 
                #print(str(repV) + ' '+str(v) + ' '+ str(w))
                if arrV[w].mergeTime == -1:
                    arrV[w].mergeTime = currE.edgeWeight
                if arrV[repW].mergeTime == -1:
                    arrV[repW].mergeTime = currE.edgeWeight
                for j in range(n):
                    if arrV[j].rep == repV:
                        arrV[j].rep = repW      
                        if arrV[j].death == -1: # update vertex death time
                            arrV[j].death = arrE[i].edgeWeight
                            arrV[j].merge = repW
                        elif currE.edgeWeight == arrV[j].mergeTime:
                            arrV[j].merge = repW
                branchCounter += get_last(arrV[repV].branchSize)
                arrV[repV].branchSize.append(0)
                arrV[repW].branchSize.append(get_last(arrV[repW].branchSize) +branchCounter)
                arrV[repV].branchTime.append(currE.edgeWeight)
                arrV[repW].branchTime.append(currE.edgeWeight)

# count component sizes 
for i in range(n):
    arrV[arrV[i].rep].componentSize +=1

for i in range(n):
    currV = arrV[i]
    currLen = len(currV.branchTime)
    #print(str(i) +' ' + str(currV.branchTime) + ' ' + str(currLen))
    for j in range(currLen):
        if get(currV.branchTime, j) != get(currV.branchTime, j+1):
            arrV[i].uniqueBranchTime.append(get(currV.branchTime,j))
            arrV[i].uniqueBranchSize.append(get(currV.branchSize,j))

for i in range(n):
        #print('{:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>20} {:>20} {:>20} {:>20}'.format(str(i), str(arrV[i].componentSize),str(arrV[i].mergeTime), str(arrV[i].rep), str(arrV[i].degree),str(arrV[i].death) , str(arrV[i].merge),   str(arrV[i].branchSize),str(arrV[i].branchTime), str(arrV[i].uniqueBranchSize), str(arrV[i].uniqueBranchTime)  ))
        sys.stdout.write(str(1)+","+str(arrV[i].degree)+","+str(arrV[i].uniqueBranchTime[len(arrV[i].uniqueBranchTime)-1]))
        #sys.stdout.write('{:>5} {:>5} {:>5}'.format(str(1), str(arrV[i].degree), str(arrV[i].uniqueBranchTime[len(arrV[i].uniqueBranchTime)-1])))
        #print('{:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>20} {:>20}'.format(str(i), str(arrV[i].componentSize),str(arrV[i].mergeTime), str(arrV[i].rep), str(arrV[i].degree),str(arrV[i].death) , str(arrV[i].merge),   str(arrV[i].uniqueBranchSize), str(arrV[i].uniqueBranchTime)  ))
        #sys.stdout.write('{:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5}'.format(str(i), str(arrV[i].componentSize),str(arrV[i].mergeTime), str(arrV[i].rep), str(arrV[i].degree),str(arrV[i].death) , str(arrV[i].merge)))
        sys.stdout.write('\n')
