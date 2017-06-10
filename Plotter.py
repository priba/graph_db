import networkx as nx
import matplotlib.pyplot as plt


def plot_graph(g, show=False, save_path=''):
    fig = plt.figure()
    nx.draw(g, pos={k: v['coord'] for k, v in g.node.items()})
    if show:
        plt.show()
    fig.savefig(save_path)