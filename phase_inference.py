
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--phase", type=str, help="phase file for the linkage group, created using genovect-batch, see README.txt for format notes")
parser.add_argument("-c", "--clusters", type=str, help="cluster-tab-marker list for all markers in the dataset, note clusters must be listed in the proper order!")
parser.add_argument("-n", "--num_progeny", type=int, help="number of progeny in the family")
args = parser.parse_args()


class cluster: 
	"""this class represents a cluster location in the marker order """
	"""within these clusters, the initial imputation will take place"""
	"""a consensus phase vector for the cluster will be output, and """
	"""it may still include missing genotypes, where no data present"""
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

#use the following to 1. find the nulls and unstack them
# then make a series with rows as the numbers and columns as the index
NaN = np.nan
d=[[11.4,1.3,2.0, NaN],[11.4,1.3,NaN, NaN],[11.4,1.3,2.8, 0.7],[NaN,NaN,2.8, 0.7]]
df = pd.DataFrame(data=d, columns=['A','B','C','D'])
df_null = df.isnull().unstack()
t = df_null[df_null]
s = pd.Series(t.index.get_level_values(1), t.index.get_level_values(0))



	def first_fill(self):
		""" this imputes a phase for NaN values that have matches up and down stream"""


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
	phase_dat = pd.read_csv(args.phase, names=df_header)

	"""read in the cluster designations """
	cluster_dat = pd.read_csv(args.clusters)

	order = cluster_dat['cluster'].drop_duplicates()

	""" for each of the clusters in the order, initiate a cluster class instance """
	""" run the .members() .phase_dat() .consensus_phase() for each class """
	""" call the .consensus_phase for each cluster, and add it to a new consensus df """






######## for development
num_progeny = 85
progeny_head = ['P_%s' % ( d+1) for d in range(0,num_progeny)]

df_header = ['marker']
df_header.extend(progeny_head)

phase_dataframe = pd.read_csv('example_phase_hq.f', names=df_header)
cluster_dataframe = pd.read_table('cluster_members.txt')
order = cluster_dataframe['cluster'].drop_duplicates()

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

or column in list(consensus_count.columns):
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

	