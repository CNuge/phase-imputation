

###################
# This is a work in progress currently
###################

The goal of this program is to leverage the new linkage mapping technique we are employing, 
in order to create an input dataset of high quality for qtl analysis, and various
statistical modelling techniques I will employ. These methods are not tolerant of missing
genotypes, so we will need to impute missing data for certain instances. Since data exists
in a linkage map, we have more information to work with than programs such as fastPHASE
which make imputations informed by LD and haplotype clustering. 

Markers placed in clusters lend themselves to making a consensus haplotype for the given
cluster. Consider the following hypothetical zero recombination cluster, ZRC_1. Any one
marker has missing genotypes and lacks a full phase vector necessary for modelling. These
markers all sit in the same cluster (cM location) on the linkage map, so their genotypes
can be merged to create a full phase vector for the given ZRC. 

ZRC_1

	M1 H-HAHAAAAA-HAHH-
	M2 HAHAH-AAAAHHAHHH
	M3 HAHAHAAAAAHH-HHH

ZRC_1  HAHAHAAAAAHHAHHH


The general idea of this algorithm is simple, it must be thorough in its consideration of 
certain fringe cases, such as when: 
1. There is disagreement between markers for an individual's phase 
	- mode will be taken, ties will be dealt with as well
2. All markers in a cluster lack a genotype for a given individual
	- will look at the clusters up and downstream to see if phase matches
	- if they do not, poll the other individuals for matches up and down
3. there is only one marker in the cluster
	- need to look at the adjacent clusters in manner of 2.

Notes on steps taken and progress made will be kept here (and on paper). Upon completion
I will turn these into a useful docstring.


New Fringe case:

- a individual of all '-' for the first or last cluster in the order, need to treat this so
that it considers the only existing neighbour and other individuals recomb/non-recomb ratios