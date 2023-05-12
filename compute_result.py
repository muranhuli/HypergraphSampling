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
import statistics

filepath = './datasets/hypergraph/'
file_list = 'NDCC TaMS MaAn WaTr ThMS TrCl CoGe CoDB'.split()

# x是sample node degree list， y是Avgdeg
def NMSE(x,y):
    squares = [(info - y) ** 2 for info in x]
    mean_square = sum(squares) / len(squares)
    return mean_square/y


for algorithm_index in range(4):
    wb= openpyxl.Workbook()
    for filename in file_list:
        ws = wb.create_sheet(filename)
        ws.append(['Range','Node NMSE', 'Unique Node NMSE', 'Avgdeg', 'Edge NMSE', 'Unique Edge NMSE', 'Avgcardi'])
        graph_path = filepath + filename
        G0 = Hypergraph(graph_path)
        
        degree =[]
        for i in G0.get_nodes():
            degree.append(G0.get_degree(i))
            
        cardi = []
        for i in G0.get_edges():
            cardi.append(G0.get_length_edge(i))
        if algorithm_index == 0:
            S = RandomWalkSampler()
            result_file_path = './result/randomwalksampler/'
        elif algorithm_index ==1:
            S = RandomWalkSamplerWithNoLazy()
            result_file_path = './result/randomwalkwithNoLazy/'
        elif algorithm_index ==2:
            S = RandomWalkSamplerWithMH()
            result_file_path = './result/randomwalkwithMH/'
        elif algorithm_index ==3:
            S = RandomWalkSamplerWithMHNormalization()
            result_file_path = './result/randomwalkwithMHNormalization/'
        avg_deg =statistics.mean(degree)
        avg_cardi = statistics.mean(cardi)
        with open(result_file_path+filename+'.txt') as f:
            data  =f.read().split('\n')
            sample_node =[int(i) for i in data[2].split()]
            sample_node_index = [int(i) for i in data[3].split()]
            sample_unique_node = [int(i) for i in data[4].split()]
            sample_unique_node_index =[int(i) for i in data[5].split()]
            sample_node_deg = []
            sample_unique_node_deg = []
            for i in sample_node:
                sample_node_deg.append(G0.get_degree(i))
            for i in sample_unique_node:
                sample_unique_node_deg.append(G0.get_degree(i))
            
            sample_edge = [int(i) for i in data[6].split()]
            sample_edge_index = [int(i) for i in data[7].split()]
            sample_unique_edge = [int(i) for i in data[8].split()]
            sample_unique_edge_index = [int(i) for i in data[9].split()]
            sample_edge_cardi = []
            sample_unique_edge_cardi = []
            for i in sample_edge:
                sample_edge_cardi.append(G0.get_length_edge(i))
            for i in sample_unique_edge:
                sample_unique_edge_cardi.append(G0.get_length_edge(i))
            
            
            for i in range(len(sample_node_index)):
                nmse1 = NMSE(sample_node_deg[:sample_node_index[i]],avg_deg)
                nmse2 = NMSE(sample_unique_node_deg[:sample_unique_node_index[i]],avg_deg)
                nmse3 = NMSE(sample_edge_cardi[:sample_edge_index[i]],avg_cardi)
                nmse4 = NMSE(sample_unique_edge_cardi[:sample_unique_edge_index[i]],avg_cardi)
                result = [f'(0, {(i+1)*100})',nmse1,nmse2,avg_deg,nmse3,nmse4,avg_cardi]
                ws.append(result)
    ws = wb['Sheet']
    wb.remove(ws)
    wb.save(f'./result/result/{S.__class__.__name__}.xlsx')
    print(f'{S.__class__.__name__}.xlsx has been generated!')  