

""" take data in the format:
Linkage_group cluster marker

and return a file for each linkage group containing only:

cluster	 marker

"""

def load_lines(cluster_file):
	"""load a tab delimited file into memory as a list of lines"""
	list_of_lines = []
	with open(cluster_file) as file:
		for line in file:
			strip_line = line.rstrip()
			split_line = strip_line.split('\t')
			list_of_lines.append(split_line)
	return list_of_lines


def get_list_of_lgs(cluster_list):
	set_of_clusters = []
	for line in cluster_list:
		if line[0] in set_of_clusters:
			continue
		else:
			set_of_clusters.append(line[0])
	return set_of_clusters


def make_files(list_of_names, extension, headerline=''):
	for name in list_of_names:
		filename = name + extension
		file = open(filename, 'a')
		file.write(headerline)
		file.close()

def split_to_files(cluster_list , extension):
	for line in cluster_list:
		filename = line[0] + extension
		output = '%s\t%s\n' % (line[1], line[2])
		file = open(filename, 'a')
		file.write(output)
		file.close()




if __name__ == '__main__':
	
	female_dat = load_lines('female_clusters.txt')
	female_lgs = get_list_of_lgs(female_dat)
	headerline = 'cluster\tmarker\n'
	make_files(female_lgs, '_clusterdat.txt', headerline)
	split_to_files(female_dat, '_clusterdat.txt')

	
	male_dat = load_lines('male_clusters.txt')
	male_lgs = get_list_of_lgs(male_dat)
	headerline = 'cluster\tmarker\n'
	make_files(male_lgs, '_clusterdat.txt', headerline)
	split_to_files(male_dat, '_clusterdat.txt')


	