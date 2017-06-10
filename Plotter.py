import networkx as nx
import matplotlib.pyplot as plt


def plot_graph(g):
    nx.draw(g, pos={k: v['coord'] for k, v in g.node.items()})
    plt.show()
