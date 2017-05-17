
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import argparse


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
	""" a class to represent the linkage group, and fill in missing values"""
	def __init__(self, order, data):
		""" read in the order and a dataframe of the consensus phase data"""
		self.order = order
		self.phase_data = data
	
	def missing_data(self):
		""" build a series, listing all the df locations with nan values"""
		""" this can target further computations to the needed locations """
		""" stores the list as self.missing"""
		missing_data_search = self.phase_data.isnull().unstack()
		missing_data_true = missing_data_search[missing_data_search]
		self.missing = pd.Series(missing_data_true.index.get_level_values(1), missing_data_true.index.get_level_values(0))

	def fill_end_of_df(self, end_index):

	def fill_adjacent_same(self):
		""" this imputes a phase for NaN values that have matches up and down stream"""
		""" when this is done, remove these from the missing data series """
#####
#this chunk needs testing
#####
		for location in range(0,len(self.missing)):
			if (self.missing[location] == 0) or (self.missing[location] == (len(self.phase_data)-1)):
				self.fill_end_of_df(self.missing[location])
				continue
			else:
				above = self.phase_data[self.missing.index[marker]][self.missing[marker]-1]
				below = self.phase_data[self.missing.index[marker]][self.missing[marker]+1]
				if above == below:
					self.phase_data[self.missing.index[marker],self.missing[marker]] = above

			# col = self.missing.index[marker]
			# row = self.missing[marker]
			#index is col, if one above == one below index of marker, impute
			#then remove from the self.missing series
			#else contine
cluster_consensus_phase_df[missing_series.index[0]][missing_series[0]]
	def count_matches(self):
		""" scan through the phase changes dataframe, counting matches with """
		""" the cluster above and the cluster below for each cluster"""
		""" store this in a list of tuples to be accessed by the filling"""

if __name__ == '__main__':
	""" turn the number of progeny into a list of names"""
	progeny_head = ['P_%s' % ( d+1) for d in range(0,args.num_progeny)]
	df_header = ['marker']
	df_header.extend(progeny_head)
	
	"""read in the phase data """
	phase_dataframe = pd.read_csv(args.phase, names=df_header)

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

	#take the cluster consensus_phase_df and manipulate it with the LG class
	#in order to impute the missing values



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


#this is self.missing
missing_data_search = cluster_consensus_phase_df.isnull().unstack()
missing_data_true = missing_data_search[missing_data_search]
missing_series= pd.Series(missing_data_true.index.get_level_values(1), missing_data_true.index.get_level_values(0))

cluster_consensus_phase_df[missing_series.index[0]][missing_series[0]]



#the cluster_consensus_phase_df above contains the data for the
#consensus phases.

#I've added in many different kind of missing phases, including:
#	- on the end
# 	- two in a row in the middle
#	- two in a row on the end







##test code##
#for consensus
name = 'X4'
member_markers = cluster_dataframe[ cluster_dataframe['cluster'] == name ]
phase = phase_dataframe[ phase_dataframe['marker'].isin(member_markers['marker'])]
phase = phase.replace('-', np.nan)
consensus = phase
consensus['marker'] = [name for x in range(0,len(consensus['marker']))]
consensus_count = consensus.apply(pd.value_counts)

consensus_phase = consensus_count.idxmax()
column = 'P_2'

for column in list(consensus_count.columns):
	counts = consensus_count[column]
	num_max = counts[counts == counts.max()]
	if len(num_max) > 1:
		consensus_phase.ix[column] = np.nan




#idea: if the inverse


df[df['A'] == df['A'].max()]

#The warning offers a suggestion to rewrite as follows:

#df.loc[df['A'] > 2, 'B'] = new_val


#Empty if nothing has 2+ occurrences.
consensus = phase.mode()
phase.value_counts()
phase.apply(pd.value_counts)

	