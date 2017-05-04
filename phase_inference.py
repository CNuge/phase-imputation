

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--phase", type=str, help="phase file for the linkage group, created using genovect-batch, see README.txt for format notes")
parser.add_argument("-c", "--clusters", type=str, help="cluster-tab-marker list for all markers in the dataset")
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
		consensus_count.idxmax()
		
		#above returns the maximal value, for ties it doesn't find them
		#can compare to the other values in index if their index == 'H', 'A' or 'V' 
		# if they're equal , then change the value to NaN
		consensus_count.index

		


		#if less than 2 count for each, it returns an NaN, need a better way, this becomes cumbersome

		#here exception handling is needed
			#1. what if no values? --> make it an NaN
			#2. if a tie... make it an NaN? then the next steps can impute it through comparison

##test code##
#for consensus
name = 'X4'
member_markers = cluster_dataframe[ cluster_dataframe['cluster'] == name ]
phase = phase_dataframe[ phase_dataframe['marker'].isin(member_markers['marker'])]
phase = phase.replace('-', np.nan)
consensus = phase
consensus['marker'] = [name for x in range(0,len(consensus['marker']))]
consensus_count = consensus.apply(pd.value_counts)

#idea: if the inverse


df[df['A'] == df['A'].max()]

#The warning offers a suggestion to rewrite as follows:

#df.loc[df['A'] > 2, 'B'] = new_val


#Empty if nothing has 2+ occurrences.
consensus = phase.mode()
phase.value_counts()
phase.apply(pd.value_counts)
if __name__ == '__main__':
	""" turn the number of progeny into a list of names"""
	progeny_head = ['P_%s' % ( d+1) for d in range(0,args.num_progeny)]
	df_header = ['marker']
	df_header.extend(progeny_head)
	
	"""read in the phase data """
	phase_dat = pd.read_csv(args.phase, names=df_header)

	"""read in the cluster designations """
	cluster_dat = pd.read_csv(args.clusters)


######## for development
	num_progeny = 85
	progeny_head = ['P_%s' % ( d+1) for d in range(0,num_progeny)]

	df_header = ['marker']
	df_header.extend(progeny_head)

	phase_dat = pd.read_csv('example_phase_hq.f', names=df_header)
	cluster_dat = pd.read_table('cluster_members.txt')





	