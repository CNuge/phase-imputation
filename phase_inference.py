
#TO DO: - recursive call in fill_ends_of_df to handle large missing data amounts
#		- search for use of np.isnan -  this is where the problems are happening, find a fix!
#		- recursive call in impute missing, ~line 129 (to handle really sparse data)
#		- test the linkage_group functionality 

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--phase", type=str, help="phase file for the linkage group, created using genovect-batch(or another phasing program), see README.txt for format notes")
parser.add_argument("-c", "--clusters", type=str, help="cluster-tab-marker list for all markers in the dataset, note clusters must be listed in the proper order!")
parser.add_argument("-n", "--num_progeny", type=int, help="number of progeny in the family")
args = parser.parse_args()


class cluster: 
	"""this class represents a cluster location in the marker order """
	"""within these clusters, the initial imputation will take place"""
	"""a consensus phase vector for the cluster will be output, and """
	"""it may still include missing genotypes, where no data is present"""
	"""or where the two phases are present in equal numbers (tie) """
	def __init__(self, cluster_name):
		""" initiate, set name of cluster """
		self.name = cluster_name
	def members(self, cluster_dataframe):
		""" grab a list of the member markers from the cluster df"""
		""" I'm coding storage 2 ways here, not sure which will be"""
		""" more efficient, delete if redundant"""
		self.member_markers = cluster_dataframe[ cluster_dataframe['cluster'] == self.name ]
		self.marker_list = list(self.member_markers['marker']) #not used yet
	def phase_dat(self, phase_dataframe):
		"""grab the phase data for the markers in the cluster"""
		self.phase = phase_dataframe[ phase_dataframe['marker'].isin(self.member_markers['marker'])]
		self.phase = self.phase.replace('-', np.nan)
	def consensus_phase(self):
		""" take the mode of the columns, changing the marker column to the cluster's name"""
		pd.options.mode.chained_assignment = None #silence assignment warning
		consensus = self.phase #make a copy of the phase dataframe to mutate
		consensus['marker'] = self.name #make the first column equal the clusters name
		consensus_count = consensus.apply(pd.value_counts) #count occurances of each string
		self.consensus_phase = consensus_count.idxmax()
		"""do a quick scan of the columns, count the occurances of the max value"""
		""" if the count exceeds 1, then there are ties for max, and nan is returned """
		for column in list(consensus_count.columns):
			counts = consensus_count[column]
			num_max = counts[counts == counts.max()]
			if len(num_max) > 1:
				self.consensus_phase[column] = np.nan


class linkage_group:
	""" a class to represent the linkage group, and impute missing values"""
	def __init__(self, order, data):
		""" read in the order and a dataframe of the consensus phase data"""
		self.order = order
		self.phase_data = data

	def missing_data(self):
		""" build a series, listing all the df locations with nan values"""
		""" this targets further computations to the needed locations"""
		""" stores the list as self.missing"""
		missing_data_search = self.phase_data.isnull().unstack()
		missing_data_true = missing_data_search[missing_data_search]
		self.missing = pd.Series(missing_data_true.index.get_level_values(1), missing_data_true.index.get_level_values(0))

	def fill_ends_of_df(self, col_index, row_index):
		""" fill the first or last clusters in the dataframe with the only flank's value """
		if row_index == 0:
			""" filling top line"""
			below = self.phase_data[col_index][row_index+1]
			""" one layer of double check, if more missing gts, will need a recursive search here"""
			if np.isnan(below)  == True:
				below = self.phase_data[col_index][row_index+2]
			self.phase_data[col_index][row_index] = below		
		else:
			above = self.phase_data[col_index][row_index-1]
			if np.isnan(above)  == True:
				above = self.phase_data[col_index][row_index-2]			
			self.phase_data[col_index][row_index] = above
			

	def count_matches(self, position, row_index, col_index):
		""" count matches with the cluster above and the cluster below for each missing spot"""
		""" return direction with more matches"""
		position_phase = self.phase_data.iloc[row_index]
		above_phase = self.phase_data.iloc[row_index -1]
		below_phase = self.phase_data.iloc[row_index +1]

		above_matches = 0
		below_matches = 0
		for idx, phase in enumerate(position_phase):
			if above_phase[idx] == phase:
				above_matches +=1
			if below_phase[idx] == phase:
				below_matches +=1
		if above_matches > below_matches:
			return 'above'
		elif above_matches < below_matches:
			return 'below'
		else:
			""" if above and below matches are equal, return one of the two randomly """
			""" print a flag to alter the user of this behaviour """
			print('%s filled at random, equal above and below matches for position %s\n' % (position_phase.marker , col_index))
			rand_choices = ['above', 'below']
			return random.choice(rand_choices)

	def impute_missing(self):
		""" this imputes a phase for NaN values that have matches up and down stream"""
		""" when this is done, remove these from the missing data series """
		for location in range(0,(len(self.missing))):
			col_index = self.missing.index[location]
			row_index = self.missing.iloc[location]
			if (row_index == 0) or (row_index == (len(self.phase_data)-1)):
				"""pull out missing data on the edges, and pass to other function"""
				self.fill_ends_of_df(col_index, row_index)
				continue
			else:
				above = self.phase_data[col_index][row_index-1]
				below = self.phase_data[col_index][row_index+1]
				if above == below:
					self.phase_data[col_index][row_index] = above
					continue
				else:
					closer_match = self.count_matches(location, row_index, col_index)
					#need a recursive function call here as well!
					if closer_match == 'above':
						
						if np.isnan(above) == True:
							self.phase_data[col_index][row_index] = above
						else:
							two_above = self.phase_data[col_index][row_index-2]
							self.phase_data[col_index][row_index] = two_above
					elif closer_match == 'below':
						if np.isnan(below) == True:
							self.phase_data[col_index][row_index] = below
						else:
							two_below = self.phase_data[col_index][row_index+2]
							self.phase_data[col_index][row_index] = two_below

	def write_phase(self, output_name):
		""" write imputed phase file to output"""
		print('writing phase data to file %s' % (output_name))
		self.phase_data.to_csv(output_name, header=False, index=False, na_rep = '-')


if __name__ == '__main__':
	"""turn the number of progeny into a list of names"""
	progeny_head = ['P_%s' % ( d+1) for d in range(0,args.num_progeny)]
	df_header = ['marker']
	df_header.extend(progeny_head)
	
	"""read in the phase data """
	phase_dataframe = pd.read_csv(args.phase, names=df_header)

	output_name = 'IMPUTED_' + args.phase
	"""read in the cluster designations """
	cluster_dataframe = pd.read_csv(args.clusters)

	order = cluster_dataframe['cluster'].drop_duplicates()

	cluster_consensus_phase_df = DataFrame(data=None, columns=df_header)
	for pos in order:
		cluster_dat = cluster(pos)
		cluster_dat.members(cluster_dataframe)
		cluster_dat.phase_dat(phase_dataframe)
		cluster_dat.consensus_phase()
		cluster_consensus_phase_df = cluster_consensus_phase_df.append(cluster_dat.consensus_phase, ignore_index=True)

	#initiate the linkage group class instance
	LG_phase_data = linkage_group(order, cluster_consensus_phase_df)
	#look for missing data
	LG_phase_data.missing_data()
	#optimistic, but if no missing data then skip the impute step and go straight to print
	if len(LG_phase_data.missing) == 0:
		LG_phase_data.write_phase(output_name)
	#or impute the missing data and then print the output
	else:
		LG_phase_data.impute_missing()
		output_name = 'test.txt'
		LG_phase_data.write_phase(output_name)


###################################################
###################################################
###################################################
###################################################
###################################################

######## for development
num_progeny = 85
progeny_head = ['P_%s' % ( d+1) for d in range(0,num_progeny)]

df_header = ['marker']
df_header.extend(progeny_head)

phase_dataframe = pd.read_csv('example_phase_hq.f', names=df_header)
cluster_dataframe = pd.read_table('cluster_members.txt')
order = cluster_dataframe['cluster'].drop_duplicates()

cluster_consensus_phase_df = DataFrame(data=None, columns=df_header)
for pos in order:
	cluster_dat = cluster(pos)
	cluster_dat.members(cluster_dataframe)
	cluster_dat.phase_dat(phase_dataframe)
	cluster_dat.consensus_phase()
	cluster_consensus_phase_df = cluster_consensus_phase_df.append(cluster_dat.consensus_phase, ignore_index=True)


cluster_consensus_phase_df[missing_series.index[0]][missing_series[0]]



#the cluster_consensus_phase_df above contains the data for the
#consensus phases.

#I've added in many different kinds of missing phases, including:
#	- on the end
# 	- two in a row in the middle
#	- two in a row on the end

cluster_consensus_phase_df.to_csv('compare.txt')


###########
#this is self.missing
missing_data_search = cluster_consensus_phase_df.isnull().unstack()
missing_data_true = missing_data_search[missing_data_search]
missing_series= pd.Series(missing_data_true.index.get_level_values(1), missing_data_true.index.get_level_values(0))

col_index = missing_series.index[location]

for location in range(0,len(missing_series)):
	print(missing_series[location])
	if (missing_series[location] == 0) or (missing_series[location] == (len(cluster_consensus_phase_df)-1)):
		self.fill_end_of_df(missing_series[location])
		continue
	else:
		above = cluster_consensus_phase_df[missing_series.index[location]][missing_series[location]-1]
		below = cluster_consensus_phase_df[missing_series.index[location]][missing_series[location]+1]
		if above == below:
			cluster_consensus_phase_df[missing_series.index[location]][missing_series[location]] = above


cluster_consensus_phase_df[missing_series.index[0]][missing_series[0]]
	
position_phase = cluster_consensus_phase_df.iloc[missing_series[position]]
above_phase = cluster_consensus_phase_df.iloc[missing_series[position] -1]
below_phase = cluster_consensus_phase_df.iloc[missing_series[position] +1]

above_matches = 0
below_matches = 0
for idx, phase in enumerate(position_phase):
	if above_phase[idx] == position_phase:
		above_matches +=1
	if below_phase[idx] == position_phase:
		below_matches +=1

##############




	