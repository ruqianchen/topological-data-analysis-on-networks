# reference
# http://stackoverflow.com/questions/17242828/python-subprocess-and-running-a-bash-script-with-multiple-arguments

# README
# This file runs randomGraphGenerator.py with n fixed and with every p in the input p array.
#
# Modification: 
## can modify to take an array of n as well. 
## can modify to auto generate p under some different distribution.


import subprocess
import numpy as np
import glob 

input_files = sorted(glob.glob('randA*'))

i = 0
while(i<len(input_files)):
	stdin_file = input_files[i]
	# if confusion, can replace foo with str(foo) 
	p = stdin_file[5:9]
	with open('randB'+ p +'.csv', 'w') as f:
		with open( stdin_file , 'r') as g:
			subprocess.call(["python", "./unweightedHBD.py"], stdin = g, stdout = f)
	i = i+1
