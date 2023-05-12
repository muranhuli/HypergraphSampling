import random
import numpy as np
from typing import Union, Tuple
from tools import *
import itertools

HGraph = type(Hypergraph())


class RandomWalkSamplerWithMHNormalization(Sampler):

    def __init__(self, number_of_nodes: int = 100, seed: int = 22, step: int = 100):
        self._sample_data = SampleData(step)
        self._number_of_nodes = number_of_nodes
        self._seed = seed
        self._set_seed()
        self._sample_count=1
        self._N=dict()
        self._NeiCount=dict()

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
        
        # Count the number of neighbor vertices of a vertex
        # for i in range(self.backend.get_number_of_edges(graph)):
        #     edge = self.backend.get_node(graph, i)
        #     for j in itertools.combinations(edge,2):
        #         if j[0] not in self._NeiCount:
        #             self._NeiCount[j[0]]=dict()
        #         if j[1] not in self._NeiCount[j[0]]:
        #             self._NeiCount[j[0]][j[1]]=0
        #         self._NeiCount[j[0]][j[1]]+=1
                
        #         if j[1] not in self._NeiCount:
        #             self._NeiCount[j[1]]=dict()
        #         if j[0] not in self._NeiCount[j[1]]:
        #             self._NeiCount[j[1]][j[0]]=0
        #         self._NeiCount[j[1]][j[0]]+=1

        # for i in self._NeiCount:
        #     self._N[i]=sum(self._NeiCount[i].values())
        #     self._NeiCount[i]=len(self.backend.get_node(graph, i))
            
    def _do_a_step(self, graph):
        if self._current_node not in self._N:
            self._NeiCount[self._current_node]=dict()
            for i in self.backend.get_edge(graph,self._current_node):
                edge = self.backend.get_node(graph, i)
                for j in edge:
                    if j != self._current_node:
                        if j not in self._NeiCount[self._current_node]:
                            self._NeiCount[self._current_node][j]=0
                        self._NeiCount[self._current_node][j]+=1
            self._N[self._current_node]=sum(self._NeiCount[self._current_node].values())
            
        vertices = []
        weight = []
        for i in self._NeiCount[self._current_node]:
            vertices.append(i)
            t = min(1/len(self.backend.get_edge(graph,self._current_node)),1/len(self.backend.get_edge(graph,i)))
            weight.append(self._NeiCount[self._current_node][i]/self._N[self._current_node]*t)
        
        self._current_node = random.choices(vertices,weights = weight,k =1)[0]
        self._sample_data.access_unique_node(self._current_node)
        self._sample_data.sample_node(self._current_node)
        self._sample_data.sample_unique_node(self._current_node)
        
        edges = []
        weight = []
        for i in self.backend.get_edge(graph,self._current_node):
            edges.append(i)
            t = min(1/len(self.backend.get_node(graph,i)),1/len(self.backend.get_node(graph,self._current_edge)))
            weight.append(t)
            
        self._current_edge = random.choices(edges,weights = weight,k =1)[0]
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