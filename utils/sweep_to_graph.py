#!/usr/bin/python
#   Usage: ./sweep_to_graph.py SWEEP_FILE.sweep [-no_clean]
#    -no_clean tells sweep_to_graph to leave intermediate .table files

# Get modules
import sys
import os


# Read input file's name from command line
inFileName = sys.argv[1]

# Look for options
clean = 1
if (len(sys.argv) >= 3):
	for arg in sys.argv[2:]:
		if arg == "-no_clean":
			clean = 0
outFileName = inFileName[:-6] + "-sweep.table"
graphName = inFileName[:-6] + "-sweep.png"

# Open Files
inFile = open(inFileName, 'r')
outFile = open(outFileName, 'w')
gnuplotFile = open('tmp.gnuplot', 'w')

# Read file into big list
lines = inFile.readlines()

# Remove comment lines
toKill = []
for i in range(len(lines)):
        tokens = lines[i].split()
        if (tokens[0][0] == '#'):
                toKill.append(i)
toKill.reverse()
for i in toKill:
        del lines[i]

# Make list for data
samples = []

# Loop over lines
for i in range(len(lines)):
        tokens = lines[i].split()
	# Look for the baseline run (single core)
	if (tokens[0] == '1' and tokens[1] == '1'):
		baseline = float(tokens[5])
	else:
		# Hold important data as a 6-tuple
		samples.append( (int(tokens[0]), int(tokens[1]), float(tokens[5]), float(tokens[6]), float(tokens[7]), float(tokens[8])))

runningMax = 0
# Loop over the samples
for i in samples:
	# Find total number of cores
	NCORES = i[0] * i[1]
	# Compute the ideal runtime based on the baseline and number of cores
	iTime = baseline / float(NCORES)
	# Write to file tasks, threads, mean eff, min eff, peak eff, and normalized standard deviation
	outFile.write(str(i[0]) + "\t" + str(i[1]) + "\t" + str(iTime / i[2]) + "\t" + str(iTime / i[3]) + "\t" + str(iTime / i[4]) + "\t" + str(i[5]) + "\n")
	# Find highest Threads value
	runningMax = max(i[1], runningMax)

# Create gnuplot command file
gnuplotFile.write("set term png; set xrange [1:" + str(runningMax) + "]; set yrange [0:1]; set logscale x; \n")
gnuplotFile.write("set title \"HOMB Sweep on " + str(NCORES) + " Cores\"; set xlabel \"Number of Threads per Task\"; set ylabel \"Value\"; \n")
gnuplotFile.write("plot \"" + outFileName + "\" using 2:5 title 'Peak Efficiency' with lp ,\
\"" + outFileName + "\" using 2:3 title 'Average Efficiency' with lp ,\
\"" + outFileName + "\" using 2:4 title 'Worst Efficiency' with lp, \
\"" + outFileName + "\" using 2:6 title 'Normalized Standard Deviation' with lp")

# Close everything up
inFile.close()
outFile.close()
gnuplotFile.close()

# Run gnuplot
os.system("gnuplot tmp.gnuplot > " + graphName)

if (clean):
	os.system("rm " + outFileName)
os.system("rm tmp.gnuplot")
