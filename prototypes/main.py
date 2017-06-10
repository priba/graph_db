import networkx as nx
import numpy as np
from Plotter import plot_graph

VERBOSE = False

am = np.array([
    [0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0]
])

v = {
    0: [0, 0],
    1: [1, 2],
    2: [2, 0],
    3: [0.25, 1],
    4: [1.75, 1],
}

g = nx.from_numpy_matrix(am)
nx.set_node_attributes(g, 'coord', v)
g.graph['class'] = 'A'

if VERBOSE:
    plot_graph(g)

nx.write_gml(g, 'test.gml')
