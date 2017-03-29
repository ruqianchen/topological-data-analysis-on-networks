# reference
# http://stackoverflow.com/questions/23665264/use-python-to-write-csv-output-to-stdout
# http://stackoverflow.com/questions/8687568/how-to-write-a-tuple-of-tuples-to-a-csv-file-using-python

# README
# This file generates edges of erdos-renyi random graph with n and p.
# The output is a csv file. Each line indicates an edge - two vertices delimited by a single space. 

import networkx as nx 
import csv
import sys
import random
import numpy as np
random.seed(9)

#n = input("What is the number of edges? Enter a positive integer.")
#p = input("What is the probability of edges? Enter a number between 0 and 1.")

#n = input()
#p = input()

n = sys.argv[1]
p = sys.argv[2]
n = int (n)
p = float(p)
g = nx.gnp_random_graph(n,p)
edges = np.asarray(g.edges())
edges = edges + 1
 
#csv_writer = csv.writer(sys.stdout, delimiter =' ')
#csv_writer.writerows(edges)

with open("randA"+str(p)+".csv",'w') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter = ' ')
	csvwriter.writerows(edges)
