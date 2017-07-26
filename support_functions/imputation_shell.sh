#!/bin/sh
 
#note this shell is dependent on data structure in directories
# you can change it to accomidate the way you have things in folders,
# or you can adjust your data to the following:
# parent directory: containing the phase_impute.py file
# a 'cluster_assignments' directory, housing the cluster files split by linkage group
# a 'phase_data' directory with all the phase files in .csv fmt
# an empty 'imputed_phase_data' directory that the program will write files to.
# note if you pass a filename in to '-p file.txt' flag it will write an
# output of 'imputed_file.txt' to the same directory. 
# if you pass in a folder+filename '-p/phase_data/file.txt' 
# as done here, it will write a file with the same name to
# a different directory with imputed_ prefix i.e. 'imputed_phase_data/file.txt'


cd cluster_assignments
linkage_groups=$(ls * | cut -d '_' -f 1)
cd ..

mkdir imputed_phase_data

for group in $linkage_groups
do
	echo $group
	echo 'finding files'
	cluster_file_extension='_clusterdat.txt'
	phase_data_extension='phase_linkmfex-convert_' #note there are m or f extensions
	cluster_file=$group$cluster_file_extension
	phase_data=$group$phase_data_extension
	cd phase_data/
	phase_dat_file=$(ls $phase_data*)
	cd ..
	prefix='imputed_phase_data'
	newdir=$prefix$phase_data
	mkdir newdir
	echo 'running python'
	python phase_impute.py -p phase_data/$phase_dat_file -c cluster_assignments/$cluster_file -n 85
done