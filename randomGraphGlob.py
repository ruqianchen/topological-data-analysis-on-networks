# reference
# http://stackoverflow.com/questions/17242828/python-subprocess-and-running-a-bash-script-with-multiple-arguments
# http://stackoverflow.com/questions/9347004/how-do-i-redirect-stdout-to-a-file-when-using-subprocess-call-in-python

# README
# This file runs unweightedHBD.py once with an input starting as randA+foo
# For a such input, it generates randB+foo.csv


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
