import numpy as np
import scipy.stats
import random
import networkx as nx
import networkit as nk
import math
from operator import itemgetter
from typing import List, Tuple, Union
from tools.Hypergraph import Hypergraph
from tools.sample_data import SampleData

HGraph = type(Hypergraph())


def KL_divergence(p, q):
    p = np.array(p)
    q = np.array(q)
    return scipy.stats.entropy(p, q, base=2)


def JS_divergence(p, q):
    p = np.array(p)
    q = np.array(q)
    M = (p + q) / 2
    return 0.5 * scipy.stats.entropy(p, M, base=2) + 0.5 * scipy.stats.entropy(q, M, base=2)


class NodeStandardValue(object):
    """Calculation of various indicators for graph sampling
    Args:
        object (_type_): _description_
    """

    def __init__(self, graph: HGraph, sample_data: SampleData, index: int):
        self._graph = graph
        # print(index, len(sample_data.get_access_unique_node_index()), len(sample_data.get_sample_node()))
        self._access_node = sample_data.get_access_unique_node()[0:sample_data.get_access_unique_node_index()[index]]
        self._sample_node = sample_data.get_sample_node()[0:(index + 1) * 100]
        self._sample_unique_node = sample_data.get_sample_unique_node()[0:sample_data.get_sample_unique_node_index()[index]]

    def basic_statistics(self) -> Tuple[int, int, int, int]:
        """
        Graphical basic statistics: total_node_size, average_degree, maximum_degree, minimum_degree
        """
        total_node_size = self._graph.number_of_nodes()
        node = self._graph.get_nodes()
        degree = []
        for info in node:
            degree.append(self._graph.get_degree(info))
        sum_degree = sum(degree)
        average_degree = sum_degree / total_node_size
        maximum_degree = max(degree)
        minimum_degree = min(degree)
        return total_node_size, average_degree, maximum_degree, minimum_degree

    def effective_sampling_node_size_ratio(self) -> float:
        """"
        Effective sampling node number ratio
        """
        return len(self._sample_unique_node) / len(self._sample_node)

    def total_variance_distance(self) -> float:
        """"
        total variance distance
        """
        total_variance_distance = 0
        n = self._graph.number_of_nodes()
        m = self._graph.number_of_edges()
        for node in self._sample_unique_node:
            total_variance_distance += abs(self._graph.get_degree(node) / (2 * m) - 1 / n)
        total_variance_distance /= 2
        return total_variance_distance

    def KL_JS(self) -> Tuple[float, float]:
        """
        compute KL and JS
        """
        node = self._graph.get_nodes()
        degree = []
        for info in node:
            degree.append(self._graph.get_degree(info))
        sum_degree = sum(degree)
        degree = zip(node, degree)
        degree = dict(degree)
        for key in degree:
            degree[key] /= sum_degree

        sample_node_degree = dict()
        sum_sample_node_degree = 0
        for node in self._sample_unique_node:
            sample_node_degree[node] = self._graph.get_degree(node)
            sum_sample_node_degree += sample_node_degree[node]

        for key in sample_node_degree:
            sample_node_degree[key] /= sum_sample_node_degree

        p = []
        p_sample = []
        for key in sorted(degree):
            p.append(degree[key])
            if key in sample_node_degree.keys():
                p_sample.append(sample_node_degree[key])
            else:
                p_sample.append(0)

        # compute KL and JS
        KL = KL_divergence(p_sample, p)
        JS = JS_divergence(p_sample, p)
        return KL, JS

    def relative_error_of_total_node_size(self) -> float:
        """
        The relative error of the total size of nodes
        """
        total_node_size = self._graph.number_of_nodes()
        if (len(self._sample_node) - len(self._sample_unique_node)) == 0:
            return 1
        estimate_total_node_size = int(len(self._sample_node))**2 / (2 * (len(self._sample_node) - len(self._sample_unique_node)))
        relative_error_of_total_node_size = abs(total_node_size - estimate_total_node_size) / total_node_size
        return relative_error_of_total_node_size

    def relative_error_of_average_degree(self) -> float:
        """
        The relative error of average degree
        """
        total_node_size = self._graph.number_of_nodes()
        node = self._graph.get_nodes()
        degree = []
        for info in node:
            degree.append(self._graph.get_degree(info))
        sum_degree = sum(degree)
        average_degree = sum_degree / total_node_size
        estimate_average_degree = sum([self._graph.get_degree(node) for node in self._sample_unique_node]) / len(self._sample_unique_node)
        relative_error_of_average_degree = abs(estimate_average_degree - average_degree) / average_degree
        return relative_error_of_average_degree

    def variance_of_sample_node(self) -> float:
        """
        The variance of sample node
        """
        total_node_size = self._graph.number_of_nodes()
        node = self._graph.get_nodes()
        degree = []
        for info in node:
            degree.append(self._graph.get_degree(info))
        sum_degree = sum(degree)
        average_degree = sum_degree / total_node_size
        variance = 0
        for node in self._sample_unique_node:
            variance += (self._graph.get_degree(node) - average_degree)**2
        variance /= len(self._sample_unique_node)
        return variance

    # def global_clustering_coefficient(self):
    #     """
    #     global clustering coefficient
    #     """
    #     gcc_origin = nx.clustering(self._graph)
    #     gcc_sample = nx.clustering(self._graph, self._sample_unique_set)

    def geweke_score(self) -> float:
        """
        Geweke score
        """
        l = len(self._sample_unique_node)
        A = self._sample_unique_node[0:int(math.ceil(l * 0.1))]
        B = self._sample_unique_node[-int(l * 0.5):]
        A = [self._graph.get_degree(node) for node in A]
        B = [self._graph.get_degree(node) for node in B]
        Z = abs((np.mean(A) - np.mean(B)) / math.sqrt(np.var(A) + np.var(B)))
        return Z
    
class EdgeStandardValue(object):
    """Calculation of various indicators for graph sampling
    Args:
        object (_type_): _description_
    """

    def __init__(self, graph: HGraph, sample_data: SampleData, index: int):
        self._graph = graph
        self._sample_edge = sample_data.get_sample_edge()[0:(index + 1) * 100]
        self._sample_unique_edge = sample_data.get_sample_unique_edge()[0:sample_data.get_sample_unique_edge_index()[index]]

    def basic_statistics(self) -> Tuple[int, int, int, int]:
        """
        Graphical basic statistics: total_edge_size, average_cardinality, maximum_cardinality, minimum_cardinality
        """
        total_edge_size = self._graph.number_of_edges()
        edge = self._graph.get_edges()
        cardi = []
        for info in edge:
            cardi.append(self._graph.get_length_edge(info))
        sum_cardi = sum(cardi)
        average_cardi = sum_cardi / total_edge_size
        maximum_cardi = max(cardi)
        minimum_cardi = min(cardi)
        return total_edge_size, average_cardi, maximum_cardi, minimum_cardi

    def effective_sampling_edge_size_ratio(self) -> float:
        """"
        Effective sampling node number ratio
        """
        return len(self._sample_unique_edge) / len(self._sample_edge)

    def total_variance_distance(self) -> float:
        """"
        total variance distance ????
        """
        total_variance_distance = 0
        n = self._graph.number_of_nodes()
        m = self._graph.number_of_edges()
        for info in self._sample_unique_edge:
            total_variance_distance += abs(self._graph.get_length_edge(info) / (2 * m) - 1 / n)
        total_variance_distance /= 2
        return total_variance_distance

    def KL_JS(self) -> Tuple[float, float]:
        """
        compute KL and JS
        """
        edge = self._graph.get_edges()
        cardi = []
        for info in edge:
            cardi.append(self._graph.get_length_edge(info))
        sum_cardi = sum(cardi)
        cardi = zip(edge, cardi)
        cardi = dict(cardi)
        for key in cardi:
            cardi[key] /= sum_cardi

        sample_edge_cardi = dict()
        sum_sample_edge_cardi = 0
        for edge in self._sample_unique_edge:
            sample_edge_cardi[edge] = self._graph.get_length_edge(edge)
            sum_sample_edge_cardi += sample_edge_cardi[edge]

        for key in sample_edge_cardi:
            sample_edge_cardi[key] /= sum_sample_edge_cardi

        p = []
        p_sample = []
        for key in sorted(cardi):
            p.append(cardi[key])
            if key in sample_edge_cardi.keys():
                p_sample.append(sample_edge_cardi[key])
            else:
                p_sample.append(0)

        # compute KL and JS
        KL = KL_divergence(p_sample, p)
        JS = JS_divergence(p_sample, p)
        return KL, JS

    def relative_error_of_total_edge_size(self) -> float:
        """
        The relative error of the total size of nodes
        """
        total_edge_size = self._graph.number_of_edges()
        if (len(self._sample_edge) - len(self._sample_unique_edge)) == 0:
            return 1
        estimate_total_edge_size = int(len(self._sample_edge))**2 / (2 * (len(self._sample_edge) - len(self._sample_unique_edge)))
        relative_error_of_total_edge_size = abs(total_edge_size - estimate_total_edge_size) / total_edge_size
        return relative_error_of_total_edge_size

    def relative_error_of_average_cardi(self) -> float:
        """
        The relative error of average degree
        """
        total_edge_size = self._graph.number_of_edges()
        edge = self._graph.get_edges()
        cardi = []
        for info in edge:
            cardi.append(self._graph.get_length_edge(info))
        sum_cardi = sum(cardi)
        average_cardi = sum_cardi / total_edge_size
        estimate_average_cardi = sum([self._graph.get_length_edge(edge) for edge in self._sample_unique_edge]) / len(self._sample_unique_edge)
        relative_error_of_average_cardi = abs(estimate_average_cardi - average_cardi) / average_cardi
        return relative_error_of_average_cardi

    def variance_of_sample_edge(self) -> float:
        """
        The variance of sample node
        """
        total_edge_size = self._graph.number_of_edges()
        edge = self._graph.get_edges()
        cardi = []
        for info in edge:
            cardi.append(self._graph.get_length_edge(info))
        sum_cardi = sum(cardi)
        average_cardi = sum_cardi / total_edge_size
        variance = 0
        for edge in self._sample_unique_edge:
            variance += (self._graph.get_length_edge(edge) - average_cardi)**2
        variance /= len(self._sample_unique_edge)
        return variance

    # def global_clustering_coefficient(self):
    #     """
    #     global clustering coefficient
    #     """
    #     gcc_origin = nx.clustering(self._graph)
    #     gcc_sample = nx.clustering(self._graph, self._sample_unique_set)

    def geweke_score(self) -> float:
        """
        Geweke score
        """
        l = len(self._sample_unique_edge)
        A = self._sample_unique_edge[0:int(math.ceil(l * 0.1))]
        B = self._sample_unique_edge[-int(l * 0.5):]
        A = [self._graph.get_length_edge(edge) for edge in A]
        B = [self._graph.get_length_edge(edge) for edge in B]
        Z = abs((np.mean(A) - np.mean(B)) / math.sqrt(np.var(A) + np.var(B)))
        return Z