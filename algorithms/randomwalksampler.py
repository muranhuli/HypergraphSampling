import random
import numpy as np
from typing import Union, Tuple
from tools import *
from tools import Hypergraph

HGraph = type(Hypergraph())


class RandomWalkSampler(Sampler):

    def __init__(self, number_of_nodes: int = 100, seed: int = 22, step: int = 100):
        self._sample_data = SampleData(step)
        self._number_of_nodes = number_of_nodes
        self._sample_count = 1
        self._seed = seed
        self._set_seed()

    def _create_initial_node_set(self, graph, start_node):
        if start_node is not None:
            if start_node >= 0 and start_node < self.backend.get_number_of_nodes(graph):
                self._current_node = start_node
                self._current_edge = self.backend.get_random_edge(graph, self._current_node)
                self._sample_data.sample_node(self._current_node)
                self._sample_data.sample_edge(self._current_edge)
                self._sample_data.sample_unique_node(self._current_node)
                self._sample_data.sample_unique_edge(self._current_edge)
            else:
                raise ValueError("Starting node index is out of range.")
        else:
            self._current_node = random.choice(range(self.backend.get_number_of_nodes(graph)))
            self._current_edge = self.backend.get_random_edge(graph, self._current_node)
            self._sample_data.sample_node(self._current_node)
            self._sample_data.sample_edge(self._current_edge)
            self._sample_data.sample_unique_node(self._current_node)
            self._sample_data.sample_unique_edge(self._current_edge)

    def _do_a_step(self, graph):
        self._current_node = self.backend.get_random_node(graph, self._current_edge)
        self._sample_data.sample_node(self._current_node)
        self._sample_data.sample_unique_node(self._current_node)
        
        self._current_edge = self.backend.get_random_edge(graph, self._current_node)
        self._sample_data.access_unique_node(self._current_node)
        self._sample_data.sample_edge(self._current_edge)
        self._sample_data.sample_unique_edge(self._current_edge)

    def sample(self, graph: HGraph, start_node: int = None) -> Tuple[list, list, list, list, list]:
        self._deploy_backend(graph)
        self._create_initial_node_set(graph, start_node)
        while self._sample_count < self._number_of_nodes:
            self._do_a_step(graph)
            self._sample_count+=1
            self._sample_data.record(self._sample_count)
        self._sample_data.record_end(self._sample_count)
        return self._sample_data