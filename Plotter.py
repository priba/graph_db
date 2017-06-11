import networkx as nx
import matplotlib.pyplot as plt


def plot_graph(g, show=False, save_path=''):
    fig = plt.figure()
    nx.draw(g, pos={k: v['coord'] for k, v in g.node.items()})
    plt.ylim([0-0.5, 2+0.5])
    plt.xlim([0-0.5, 2+0.5])
    if show:
        plt.show()
    fig.savefig(save_path)
