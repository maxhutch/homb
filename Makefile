#==============================================
# Makefile for HOMB
# Max Hutchinson (mhutchin@psc.edu)
# created: 7/26/08
#==============================================

HOMB = homb.ex
QUIVER = quiver.ex

include config/Make.default
include config/Make.mach.${MACHINE}

default: $(HOMB)

all: $(HOMB) $(QUIVER)

$(HOMB): src/homb.c
	$(CC) $(MPIFLAGS) $(OMPFLAGS) -o $(HOMB) $(OPTFLAGS) src/homb.c

$(QUIVER): src/quiver.c
	$(CC) $(MPIFLAGS) $(OMPFLAGS) -o $(QUIVER) $(OPTFLAGS) src/quiver.c

clean:
	rm *.ex
