import os
import numpy as np
import json
import random
from typing import List, Tuple
from tools.Hypergraph import Hypergraph

HGraph = type(Hypergraph())


class HypernetxBackEnd(object):

    def __init__(self):
        pass

    def get_number_of_nodes(self, graph: HGraph) -> int:
        # Get the total number of vertices in the hypergraph
        return graph.number_of_nodes()

    def get_number_of_edges(self, graph: HGraph) -> int:
        # Get the total number of hyperedges in the hypergraph
        return graph.number_of_edges()

    def get_nodes(self, graph: HGraph) -> List:
        # Get the set of lists of vertices in the hypergraph
        return graph.get_nodes()

    def get_edges(self, graph: HGraph) -> List:
        # Get the set of lists of hyperedges in the hypergraph
        return graph.get_edges()

    def get_node(self, graph: HGraph, edge: int):
        # Get the composition of the vertices of a hyperedge
        return graph.get_node(edge)

    def get_edge(self, graph: HGraph, node: int):
        # Get the neighboring hyperedges of a vertex
        return graph.get_edge(node)

    def get_degree(self, graph: HGraph, node: int) -> int:
        # Get the degree of the vertices in the hypergraph
        return graph.get_degree(node)

    def get_edges_length(self, graph: HGraph, edge: int) -> int:
        # Get the number of vertices of a hyperedge
        return len(graph.get_node(edge))

    def get_random_edge(self, graph: HGraph, node: int) -> int:
        # Randomly select a neighboring hyperedge of a vertex
        return random.choice(graph.get_edge(node))

    def get_random_node(slef, graph: HGraph, edge: int) -> int:
        # Get a random vertex in a hyperedge
        return random.choice(graph.get_node(edge))
    
    def get_hypergraph(self,graph:HGraph):
        return graph.get_hypergraph()

    # def _check_connectivity(self, graph: HGraph):
    #     connected_component = list(graph.s_connected_components())
    #     flag = False
    #     if len(list(connected_component)) == 1:
    #         if (len(connected_component[0]) == graph.number_of_edges()):
    #             flag = True
    #     assert flag == True, "Hypergraph is not connected."

    # def check_graph(self, graph: HGraph):
    #     # self._check_connectivity(graph)
    #     self._check_indexing(graph)
