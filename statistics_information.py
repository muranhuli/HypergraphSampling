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
from typing import List, Tuple, Union

HGraph = type(Hypergraph())


def node_basic_statistics(graph: HGraph) -> Tuple[int, int, int, int]:
    """
    Graphical basic statistics: total_node_size, average_degree, maximum_degree, minimum_degree
    """
    total_node_size = graph.number_of_nodes()
    node = graph.get_nodes()
    degree = []
    for info in node:
        degree.append(graph.get_degree(info))
    sum_degree = sum(degree)
    average_degree = sum_degree / total_node_size
    maximum_degree = max(degree)
    minimum_degree = min(degree)
    return total_node_size, average_degree, maximum_degree, minimum_degree


def edge_basic_statistics(graph: HGraph) -> Tuple[int, int, int, int]:
    """
    Graphical basic statistics: total_edge_size, average_cardinality, maximum_cardinality, minimum_cardinality
    """
    total_edge_size = graph.number_of_edges()
    edge = graph.get_edges()
    cardi = []
    for info in edge:
        cardi.append(graph.get_length_edge(info))
    sum_cardi = sum(cardi)
    average_cardi = sum_cardi / total_edge_size
    maximum_cardi = max(cardi)
    minimum_cardi = min(cardi)
    return total_edge_size, average_cardi, maximum_cardi, minimum_cardi


filepath = './datasets/standardized_hypergraph/'
file_list = 'NDCC TaMS CoBi TaAU MaAn WaTr ThAU ThMS TrCl'.split()

wb = openpyxl.Workbook()
ws = wb.active
ws.append(['filename', 'total_node_size', 'average_degree', 'maximum_degree', 'minimum_degree', 'total_edge_size', 'average_cardinality', 'maximum_cardinality', 'minimum_cardinality'])
for filename in file_list:
    print(filename)
    graph_path = filepath + filename
    G0 = Hypergraph(graph_path)
    node_data = node_basic_statistics(G0)
    edge_data = edge_basic_statistics(G0)
    data = [filename] + list(node_data) + list(edge_data)
    ws.append(data)
wb.save('./result/hypergraph_statisitics_infomation.xlsx')
print('./result/hypergraph_statisitics_infomation.xlsx has been finished!')
