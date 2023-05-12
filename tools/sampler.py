import random
import numpy as np
import networkx as nx
import networkit as nk
from typing import Union
import hypernetx as hnx
from tools.backend import HypernetxBackEnd

HGraph = type(hnx.Hypergraph())

class Sampler(object):
    def __init__(self):
        pass
    
    def sample(self):
        pass
    
    def _set_seed(self):
        random.seed(self._seed)
        np.random.seed(self._seed)
        
    def _deploy_backend(self,graph:HGraph):
        # Chechking the input type
        self.backend=HypernetxBackEnd()
        # self.backend.check_graph(graph)
    