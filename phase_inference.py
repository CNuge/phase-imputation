

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--phase", type=str, help="phase file for the linkage group, created using genovect-batch, see README.txt for format notes")
parser.add_argument("-c", "--clusters", type=str, help="cluster-tab-marker list for all markers in the dataset")
args = parser.parse_args()








if __name__ == '__main__':

