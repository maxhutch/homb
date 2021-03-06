
Hybrid OpenMP MPI Benchmark
========================================================================

HOMB version 0.9 (2008 08 03)
---------------------------------

HOMB is the Hybrid OpenMP MPI Benchmark for testing hybrid codes on
multicore and SMP systems.  The code is an optimized Laplace Solver
on a 2-D grid (Point Jacobi) with optional convergence test.

The code is designed to compare the performance of MPI, OpenMP, and
hybrid codes.  It will behave as a pure MPI code when the number of
threads per task is 1 and a pure OpenMP code when the number of 
tasks is 1.

There are two general tests corespoding to three types of output:

*   Summary tests provide the statstical performance of HOMB
*   Times tests provide the raw runtimes of each task

To understand how these tests can be used to draw conclusions, it 
is recommended that the user reads the code over or simply use
summary tests output (-s).  

NOTE: all tests run the same code and only differ in output.

Job Files
------------------

Job files that compile and run HOMB are avaliable on these machines:

    PSC's Altix 4700 (Pople or Salk)
    PSC's Xeon Cluster (Muir)
    NCSA's Altix 3700 (Cobalt)
    TACC's Sun Constellation Linux Cluster (Ranger)

To Build
------------------

If there is a `Make.mach.<machine>` file for the desired machine:

    make MACHINE=<machine>

If you want to add make support for your machine, copy a file for 
another machine and change the options.

--or--

Compile with MPI and OpenMP support and desired optimization flags.
Examples:

    icc -o homb.ex -O3 -ftz -ipo -openmp -lmpi src/homb.c
    gcc -o homb.ex -O3 -fopenmp -lmpi src/homb.c

To Run
------------------

Run with MPI/OpenMP support and following args:

    -NC  val             Number of Columns in grid 
    -NR  val             Number of Rows in grid    
    -NRC val             Number of Rows and Columns in grid 
    -NITER val           Number of iterations      
    -[no_]barrier        Places MPI_Barrier at start of iterations
    -[no_]reduce         Places MPI_Reduce at end of iterations
    -s                   Summary to standard out
    -v                   Verbose to standard out
    -nh                  No header in standard out
    -vf val              File name for verbose file output
    -tf val              File name for times matrix file output
    -pc                  Print Context (settings) to standard out

Examples
--------

    mpirun -np 4 omplace -nt 4 ./homb.ex -NRC \
        -NITER 25 -vf homb-4-4-32768.out -s

Run on 16 cores with 4 tasks and 4 threads per task over
25 iterations with 512MB/core memory usage.  Outputs
all data to file and a summary to Standard Out.

    mpirun -np 4 ./homb.ex -NR 16384 -NC 16384 -NITER 10 -v

Run on 4 cores with pure MPI over 10 iterations with
512MB/core mem usage.  Outputs all data to stdout.

Utilities
---------

#### [times_to_hist.py](utils/times_to_hist.py)

This script takes a times output file from HOMB and produces a
histogram of the runtimes, allowing the user to analyze the 
distribution/variablility of the performance of the machine.

#### [times_to_chain.py](utils/times_to_chain.py)

This script takes a times output file from HOMB and produces an
animation of exclusive runtimes of the individual PEs through time, 
allowing the user to see the relationships/coupling of the PEs.
The ouput can be thought of as the PE's chained together oscillating.
For example, on can deduce the general form of MPI_Reduce. 

#### [times_to_race.py](utils/times_to_race.py)

This script takes a times output file from HOMB and produces an
animation of inclusive runtimes of the individual PEs through time, 
allowing the user to see the relationships/coupling of the PEs.
The output can be thought of as the PE's racing (but low is good).
For example, on can deduce the general form of MPI_Reduce. 

#### [times_to_covar.py](utils/times_to_covar.py)

This script takes a times output file from HOMB and produces a
matrix of the covariances of ranks to one another.  This is useful
for finding the relative coupling of tasks.

#### [sweep_to_graph.py](utils/sweep_to_graph.py)

This script takes a set of summary lines form multiple mulit-core 
runs and one single core run (of the same problem size) to plot
peak, average, and minimum performance of various MPI/OpenMP ratios

#### [sweeps_to_scales.py](utils/sweeps_to_scales.py)

This script takes a set of summary lines form multiple mulit-core 
on multiple number of total cores (sweeps) and plots the peak, mean,
and worst performance to show weak-scaling.

More info
---------

Max Hutchinson (mhutchin@psc.edu).

Creator: Max Hutchinson (mhutchin@psc.edu)

Proto-code written by: Uriel Jaroslawski, Jon Iturralde
