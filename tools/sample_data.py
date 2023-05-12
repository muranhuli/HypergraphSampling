import numpy as np
import scipy.stats
import random
import math
from operator import itemgetter
from typing import List, Tuple, Union


class SampleData(object):

    def __init__(self, step: int):
        self._step = step
        # Initialize the data to be sampled

        self._sample_node = []  # The node list recorded at each step contains duplicate nodes
        self._sample_node_index = []
        
        self._sample_edge = []
        self._sample_edge_index = []

        self._sample_unique_node = []  # Remove duplicate nodes in the sampling node list, The list collection of non-heavy symbols is ordered
        self._sample_unique_node_index = []  # Used to record every 100 samples, the range index of valid nodes

        self._access_unique_node = []  # Get the node set of deg(v), not counting duplicates
        self._access_unique_node_index = []  # Used to record every 100 samples, the range index of valid nodes

        self._sample_unique_edge = []
        self._sample_unique_edge_index = []

    def access_unique_node(self, node: int):
        if node not in self._access_unique_node:
            self._access_unique_node.append(node)

    def sample_node(self, node: int):
        self._sample_node.append(node)

    def sample_unique_node(self, node: int):
        if node not in self._sample_unique_node:
            self._sample_unique_node.append(node)

    def sample_edge(self, edge: int):
        self._sample_edge.append(edge)

    def sample_unique_edge(self, edge: int):
        if edge not in self._sample_unique_edge:
            self._sample_unique_edge.append(edge)
    
    def sample_number(self):
        # Number of samples, based on sample_node
        return len(self._sample_node)
    
    def get_access_unique_node(self):
        return self._access_unique_node
    
    def get_access_unique_node_index(self):
        return self._access_unique_node_index

    def get_sample_node(self):
        return self._sample_node
    
    def get_sample_node_index(self):
        return self._sample_node_index

    def get_sample_unique_node(self):
        return self._sample_unique_node

    def get_sample_unique_node_index(self):
        return self._sample_unique_node_index

    def get_sample_edge(self):
        return self._sample_edge

    def get_sample_edge_index(self):
        return self._sample_edge_index

    def get_sample_unique_edge(self):
        return self._sample_unique_edge

    def get_sample_unique_edge_index(self):
        return self._sample_unique_edge_index
    
    def record_to_file(self,filename):
        with open(filename,'w') as f:
            data = [str(i) for i in self._access_unique_node]
            f.write(' '.join(data)+'\n')
            data = [str(i) for i in self._access_unique_node_index]
            f.write(' '.join(data)+'\n')
            data = [str(i) for i in self._sample_node]
            f.write(' '.join(data)+'\n')
            data = [str(i) for i in self._sample_node_index]
            f.write(' '.join(data)+'\n')
            data  =[str(i) for i in self._sample_unique_node]
            f.write(' '.join(data)+'\n')
            data = [str(i) for i in self._sample_unique_node_index]
            f.write(' '.join(data)+'\n')
            data = [str(i) for i in self._sample_edge]
            f.write(' '.join(data)+'\n')
            data = [str(i) for i in self._sample_edge_index]
            f.write(' '.join(data)+'\n')
            data = [str(i) for i in self._sample_unique_edge]
            f.write(' '.join(data)+'\n')
            data = [str(i) for i in self._sample_unique_edge_index]
            f.write(' '.join(data)+'\n')
    
    # def sample_number(self):
    #     # Number of samples, based on sample_node
    #     return len(self._sample_node)

    def record(self, cnt):
        if cnt % self._step == 0:
            self._access_unique_node_index.append(len(self._access_unique_node))
            self._sample_unique_node_index.append(len(self._sample_unique_node))
            self._sample_unique_edge_index.append(len(self._sample_unique_edge))
            self._sample_node_index.append(len(self._sample_node))
            self._sample_edge_index.append(len(self._sample_edge))
    
    def record_end(self, cnt):
        if cnt % self._step != 0:
            self._access_unique_node_index.append(len(self._access_unique_node))
            self._sample_unique_node_index.append(len(self._sample_unique_node))
            self._sample_unique_edge_index.append(len(self._sample_unique_edge))
            self._sample_node_index.append(len(self._sample_node))
            self._sample_edge_index.append(len(self._sample_edge))