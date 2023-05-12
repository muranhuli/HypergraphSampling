import networkx as nx
from algorithms import *
from tools import *
from collections import Counter
from operator import itemgetter
import scipy.stats
import numpy as np
import math
import sys
import openpyxl
import pandas as pd
import os
import multiprocessing as mp


def run_algorithm(args):
    algorithm_index, filename = args
    graph_path = filepath + filename
    G0 = Hypergraph(graph_path)
    result_file_path = ""

    if algorithm_index == 0:
        S = RandomWalkSampler(int(G0.number_of_nodes() * 0.5))
        result_file_path = "./result/randomwalksampler/"
    elif algorithm_index == 1:
        S = RandomWalkSamplerWithNoLazy(int(G0.number_of_nodes() * 0.5))
        result_file_path = "./result/randomwalkwithNoLazy/"
    elif algorithm_index == 2:
        S = RandomWalkSamplerWithMH(int(G0.number_of_nodes() * 0.5))
        result_file_path = "./result/randomwalkwithMH/"
    elif algorithm_index == 3:
        S = RandomWalkSamplerWithMHNormalization(int(G0.number_of_nodes() * 0.5))
        result_file_path = "./result/randomwalkwithMHNormalization/"

    # start sample
    sample_data = S.sample(G0)
    sample_data.record_to_file(result_file_path + filename + ".txt")
    print(S.__class__.__name__, filename, "finished")


filepath = "./datasets/hypergraph/"
file_list = "MaAn WaTr ThMS TrCl CoGe CoDB".split()

tasks = [(algorithm_index, filename) for algorithm_index in range(4) for filename in file_list]

with mp.Pool() as pool:
    pool.map(run_algorithm, tasks)
