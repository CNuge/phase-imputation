
#merge all your phase files into one, adding the first part of the filename
#to the cluster names, in order to distinguish between clusters in different 
#linkage groups

files=$(ls *.csv)
for file_name in $files
do
	prefix=$(echo $file_name | cut  -d '_' -f 1)
	sed -e "s/^/$prefix/g" $file_name >> ../all_phase_data.csv
done