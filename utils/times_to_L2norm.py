#!/usr/bin/python
#  Usage: ./times_to_L2norm.py TIMES_FILE.times

# Get modules
import sys
import os

# Get input file's name
inFileName = sys.argv[1]
outFileName = inFileName[:-5] + "L2n"

# Open Files
inFile = open(inFileName, 'r')
outFile = open(outFileName, 'w')

# Read file into list of lines
lines = inFile.readlines()

# Get rid of comment lines
toKill = []
for i in range(len(lines)):
        tokens = lines[i].split()
        if (tokens[0] == '#'):
                toKill.append(i)
toKill.reverse()
for i in toKill:
        del lines[i]

tokens = lines[0].split()
nPEs = len(tokens)
times = []
covar = []
for i in range(nPEs):
	times.append([float(tokens[i])])
	covar.append([])

# Loop over lines to get times matrix
for i in range(1,len(lines)):
	# Tokenize
	tokens = lines[i].split()
	for j in range(nPEs):
		times[j].append(float(tokens[j]))

# Loop over PEs in times matrix to find Co-Variances
for i in range(nPEs):
	for j in range(nPEs):
		diffs = 0.0
		for k in range(len(lines)):
			diffs += (times[i][k] - times[j][k]) ** 2
		covar[i].append((diffs / len(lines)) ** .5)

# Loop over covar matrix to write to file
for i in range(nPEs):
	for j in range(nPEs):
		outFile.write(str(covar[i][j]) + "\t")
	outFile.write("\n")

# Close Files
inFile.close()
outFile.close()
