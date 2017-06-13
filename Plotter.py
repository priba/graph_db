import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def plot_graph(g, show=False, save_path=''):
    fig = plt.figure()
    position = {k: v['coord'] for k, v in g.node.items()}

    center = np.mean(position.values(),axis=0)
    max_pos = np.max(np.abs(position.values()-center))

    nx.draw(g, pos=position)

    plt.ylim([center[1]-max_pos-0.5, center[1]+max_pos+0.5])
    plt.xlim([center[0]-max_pos-0.5, center[0]+max_pos+0.5])

    if show:
        plt.show()
    fig.savefig(save_path)
