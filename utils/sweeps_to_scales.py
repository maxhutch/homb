#!/usr/bin/python
#   Usage: ./sweeps_to_scales.py SWEEP_FILE1.sweep SWEEP_FILE2.sweep ...

# Get modules
import sys
import os
import time

numFiles = len(sys.argv)-1

# Read input file's name from command line
inFileName = []
tableFileName = []
for i in range(numFiles):
	inFileName.append(sys.argv[i+1])
	tableFileName.append(inFileName[i][:-6] + "-sweep.table")

for i in range(numFiles):
	os.system("./sweep_to_graph.py " + inFileName[i] + " -no_clean ")

pgraphName = "peak-scales.png"
mgraphName = "mean-scales.png"
wgraphName = "worst-scales.png"
dgraphName = "deviation-scales.png"

# Make peak-scales
gnuFile = open('peak.gnuplot','w')
gnuFile.write("set term png; set xrange [1:256]; set yrange [0:1]; set logscale x; \n")
gnuFile.write("set title \"HOMB Peak Perforance Scale\"; set xlabel \"Number of Threads per Task\"; set ylabel \"Parallel Efficiency\"; \n")
gnuFile.write("plot ")
for n in tableFileName[:-1]:
	gnuFile.write("\"" + n + "\" using 2:5 title \"" + n[:-12] + "\" with lp,")
gnuFile.write("\"" + tableFileName[-1] + "\" using 2:5 title \"" + n[:-12] + "\" with lp \n")
gnuFile.close


# Make mean-scales
gnuFile = open('mean.gnuplot','w')
gnuFile.write("set term png; set xrange [1:256]; set yrange [0:1]; set logscale x; \n")
gnuFile.write("set title \"HOMB Mean Perforance Scale\"; set xlabel \"Number of Threads per Task\"; set ylabel \"Parallel Efficiency\"; \n")
gnuFile.write("plot ")
for n in tableFileName[:-1]:
	gnuFile.write("\"" + n + "\" using 2:3 title \"" + n[:-12] + "\" with lp,")
gnuFile.write("\"" + tableFileName[-1] + "\" using 2:3 title \"" + n[:-12] + "\" with lp \n")
gnuFile.close


# Make worst-scales
gnuFile = open('worst.gnuplot','w')
gnuFile.write("set term png; set xrange [1:256]; set yrange [0:1]; set logscale x; \n")
gnuFile.write("set title \"HOMB Worst Perforance Scale\"; set xlabel \"Number of Threads per Task\"; set ylabel \"Parallel Efficiency\"; \n")
gnuFile.write("plot ")
for n in tableFileName[:-1]:
	gnuFile.write("\"" + n + "\" using 2:4 title \"" + n[:-12] + "\" with lp,")
gnuFile.write("\"" + tableFileName[-1] + "\" using 2:4 title \"" + n[:-12] + "\" with lp \n")
gnuFile.close


# Make deviation-scales
gnuFile = open('dev.gnuplot','w')
gnuFile.write("set term png; set xrange [1:256]; set yrange [0:1]; set logscale x; \n")
gnuFile.write("set title \"HOMB Deviation Scale\"; set xlabel \"Number of Threads per Task\"; set ylabel \"Normalized Standard Deviation\"; \n")
gnuFile.write("plot ")
for n in tableFileName[:-1]:
	gnuFile.write("\"" + n + "\" using 2:6 title \"" + n[:-12] + "\" with lp,")
gnuFile.write("\"" + tableFileName[-1] + "\" using 2:6 title \"" + n[:-12] + "\" with lp \n")

gnuFile.close

time.sleep(10)
os.system("gnuplot peak.gnuplot > " + pgraphName)
os.system("gnuplot mean.gnuplot > " + mgraphName)
os.system("gnuplot worst.gnuplot > " + wgraphName)
os.system("gnuplot dev.gnuplot > " + dgraphName)

os.system("rm *.gnuplot")
for n in tableFileName:
	os.system("rm " + n)
