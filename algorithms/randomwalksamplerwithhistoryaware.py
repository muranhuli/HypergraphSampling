import random
import copy
import numpy as np
from typing import Union, Tuple
from tools import *
from tools import Hypergraph

HGraph = type(Hypergraph())


class RandomWalkSamplerWithHistoryAware(Sampler):

    def __init__(self, number_of_nodes: int = 100, seed: int = 22, step: int = 100):
        self._sample_data = SampleData(step)
        self._number_of_nodes = number_of_nodes
        self._seed = seed
        self._set_seed()
        self._visitedNode = []
        self._visitedEdge = []

    def _create_initial_node_set(self, graph, start_node):
        for i in range(self.backend.get_number_of_nodes(graph)):
            self._visitedNode.append(False)
        for i in range(self.backend.get_number_of_edges(graph)):
            self._visitedEdge.append(False)
        if start_node is not None:
            if start_node >= 0 and start_node < self.backend.get_number_of_nodes(graph):
                self._current_node = start_node
                self._current_edge = None
                self._sample_data.sample_node(self._current_node)
                self._sample_data.sample_unique_node(self._current_node)
            else:
                raise ValueError("Starting node index is out of range.")
        else:
            self._current_node = random.choice(range(self.backend.get_number_of_nodes(graph)))
            self._current_edge = None
            self._sample_data.sample_node(self._current_node)
            self._sample_data.sample_unique_node(self._current_node)
        self._visitedNode[self._current_node] = True

    def _do_a_step(self, graph):
        adjacent_hyperedge = self.backend.get_edge(graph, self._current_node)
        adjacent_hyperedge = [info for info in adjacent_hyperedge if not self._visitedEdge[info]]
        # tmp =[]
        # for info in adjacent_hyperedge:
        #     if self._visitedEdge[info]:
        #         tmp.append(info)
        # for info in tmp:
        #     adjacent_hyperedge.remove(info)

        if adjacent_hyperedge:
            self._current_edge = random.choice(adjacent_hyperedge)
        else:
            self._current_edge = self.backend.get_random_edge(graph, self._current_node)
        self._sample_data.sample_edge(self._current_edge)
        self._sample_data.sample_unique_edge(self._current_edge)

        vertices_set = self.backend.get_node(graph, self._current_edge)
        vertices_set = [info for info in vertices_set if not self._visitedNode[info]]
        # tmp =[]
        # for info in vertices_set:
        #     if self._visitedNode[info]:
        #         tmp.append(info)
        # for info in tmp:
        #     vertices_set.remove(info)

        if vertices_set:
            self._current_node = random.choice(vertices_set)
        else:
            self._current_node = self.backend.get_random_node(graph, self._current_edge)
        self._sample_data.access_unique_node(self._current_node)
        self._sample_data.sample_node(self._current_node)
        self._sample_data.sample_unique_node(self._current_node)

        self._visitedEdge[self._current_edge] = True
        self._visitedNode[self._current_node] = True

    def sample(self, graph: HGraph, start_node: int = None) -> Tuple[list, list, list, list, list]:
        self._deploy_backend(graph)
        self._create_initial_node_set(graph, start_node)
        while self._sample_data.sample_number() < self._number_of_nodes:
            self._do_a_step(graph)
            self._sample_data.record()
        self._sample_data.record_end()
        return self._sample_data