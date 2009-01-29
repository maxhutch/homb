#!/usr/bin/python
#
# Script to take the times output and produce a histogram
#  Usage: ./times_to_hist.py TIMES_FILE.times PE_NUMBER1 [PE_NUMBER2 ...]
#  PE_NUMBER is the number of the PE whose times you want to see (a will give you all of them)

# Get modules
import sys
import os

# Get input file's name and name output files
inFileName = sys.argv[1]
outFileName = inFileName[:-5] + "hist"
graphFileName = inFileName[:-6] + "-hist.png"


# Get the number for the PE that we care about (a is for all)
PE_NUMBERS = sys.argv[2:len(sys.argv)]

# Convert PE_NUMBERS to integers
if (PE_NUMBERS[0] != 'a'):
	for i in range(len(PE_NUMBERS)):
		PE_NUMBERS[i] = int(PE_NUMBERS[i])

# Open Files
inFile = open(inFileName, 'r')
outFile = open(outFileName, 'w')
gnuFile = open('tmp.gnuplot', 'w')

# Create list for values
values = []

# Loop through file
for line in inFile:
	# Tokenize
	tokens = line.split()
	# Look for comments
	if (tokens[0][0] == '#'):
		continue
	# Get number of tasks
	nPEs = len(tokens)
	# Translate 'a' option to all tasks
        if (PE_NUMBERS[0] == 'a'):
		PE_NUMBERS = range(nPEs)
	# Loop over tasks writing times to list and file
        for i in PE_NUMBERS:
		outFile.write(tokens[i] + '\n')
                values.append(float(tokens[i]))

# Sort times
values.sort()

# Find max and min (set to exclude extreme outliers
maxVal = values[99 * len(values) / 100]
minVal = values[len(values) / 100]
# Define spacing for 20 increments
increment = (maxVal - minVal) / 20.0

# Write gnuplot commands to file
gnuFile.write("# Command file for gnuplot created by times_to_hist.py \n")
gnuFile.write("set terminal png ; set xrange [" + str(minVal) + ":" + str(maxVal) + "] \n")
gnuFile.write("bw=" + str(increment) + " ; bin(x,width)=width*floor(x/width) \n")
gnuFile.write("plot '" + outFileName + "' using (bin($1,bw)):(1.0) smooth freq with boxes \n")

# Close files up
inFile.close()
outFile.close()
gnuFile.close()

# Run gnuplot
os.system("gnuplot tmp.gnuplot > " + graphFileName)
os.system("rm tmp.gnuplot")
os.system("rm " + outFileName)
