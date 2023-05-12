import os
import numpy as np
import json
import copy

class Hypergraph(object):
    r"""
    We use the hypernetx package to store hypergraphs.
    Since the hypergraph storage format used by hypernetx is json format, the
    So we provide tools to convert existing hypergraphs to json format.
    Current hypergraph storage format: e0=v0, v1, v2, v3, v4, ..., vn
    """
    
    def __init__(self, filename:str=None):
        if filename is not None:   
            self.hyperEdge = []
            self.hyperNode = {}
            with open(filename) as f:
                for line in f:
                    tmp_data = line.split()
                    tmp_data = [int(info) for info in tmp_data]
                    self.hyperEdge.append(tmp_data)
            for index, edge in enumerate(self.hyperEdge):
                for node in edge:
                    if node in self.hyperNode.keys():
                        self.hyperNode[node].append(index)
                    else:
                        self.hyperNode[node]=[index]
            max_node = max(self.hyperNode.keys())
            tmp =[]
            for i in range(max_node+1):
                tmp.append(self.hyperNode[i])
            self.hyperNode = copy.deepcopy(tmp)
        
    def number_of_nodes(self):
        # Get the total number of vertices in the hypergraph
        return len(self.hyperNode)
    
    def number_of_edges(self):
        # Get the total number of hyperedges in the hypergraph
        return len(self.hyperEdge)
    
    def get_nodes(self):
        # Get the set of lists of vertices in the hypergraph
        return [info for info in range(len(self.hyperNode))]
    
    def get_edges(self):
        # Get the set of lists of hyperedges in the hypergraph
        return [info for info in range(len(self.hyperEdge))]
    
    def get_degree(self, node: int):
        # Get the degree of the vertices in the hypergraph
        return len(self.hyperNode[node])
    
    def get_length_edge(self,edge:int):
        return len(self.hyperEdge[edge])

    def get_node(self,edge:int):
        # Get the composition of the vertices of a hyperedge
        return self.hyperEdge[edge]
    
    def get_edge(self, node:int):
        # Get the neighboring hyperedges of a vertex
        return self.hyperNode[node]
    
    def get_hypergraph(self):
        return self.hyperEdge, self.hyperNode
                
        
        
        
            
