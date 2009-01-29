#!/usr/bin/python
#   Usage: ./times_to_race.py TIMES_FILE.times

# Get modules
import sys
import os
import math

# Get input file name from command line and name output file
inFileName = sys.argv[1]
movieFileName = inFileName[:-6] + "-race.mpg"

# Open input file
inFile = open(inFileName, 'r')

# Read file into list of lines
lines = inFile.readlines()

# Find maximum number of leading zeroes so the "cat" command sorts in the right order
maxPadding = int(math.log(len(lines),10))

# Make lists for values and the output file's name
outFileName = []

# Get rid of comment lines
toKill = []
for i in range(len(lines)):
	tokens = lines[i].split()
	if (tokens[0] == '#'):
		toKill.append(i)
toKill.reverse()
for i in toKill:
	del lines[i]

# Get number of tasks and create values matrix
tokens = lines[0].split()
nPEs = len(tokens)
values = []
for i in range(nPEs):
	values.append([])

# Loop over lines
for i in range(len(lines)):
        # Tokenize
	tokens = lines[i].split()
	# Figure out how many leading zeroes must be added
	if (i == 0):
		padding = 0
	else:
		padding = int( math.log( i, 10))
	# Add nessesary zeroes
	zeroes = ""
	for k in range(maxPadding - padding):
		zeroes = zeroes + str(0)

	# Name and open a file for the output of a frame
	outFileName.append(zeroes + str(i) + ".crv")
	outFile = open(outFileName[i], 'w')
	# Write out task number and coresponding time value, store time in values
	for j in range(len(tokens)):
		values[j].append(float(tokens[j]))
		outFile.write(str(j) + "\t" + str(sum(values[j])) + "\n")
	# Close this particular file
	outFile.close()

# Sort values and get max and min (outlier safe)
#values.sort()
#maxVal = values[ 99 * len(values) / 100 ]
#minVal = values[ len(values) / 100 ]

# Write gnuplot command files to make pngs
for i in range(len(lines)):
	gnuplotFile = open('tmp.gnuplot', 'w')
	gnuplotFile.write("set terminal png ; set xrange [0:" + str(nPEs) + "]; set yrange[:]; \n")
	gnuplotFile.write("plot '" + outFileName[i] + "' using 1:2 with lp \n")
	gnuplotFile.close()
	# Run gnuplot
	os.system("gnuplot tmp.gnuplot > " + outFileName[i] + ".png")
	# Convert png to ppm
        os.system("pngtopnm " + outFileName[i] + ".png > " + outFileName[i] + ".ppm ")

# Make the movie
os.system("cat *.ppm | ppmtoy4m -S 420jpeg | mpeg2enc --format 3 --video-bitrate 5000 --motion-search-radius 32 --no-constraints -o " + movieFileName )

# clean up
os.system("rm *.crv")
os.system("rm *.png")
os.system("rm *.ppm")
os.system("rm tmp.gnuplot")
