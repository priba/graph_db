#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Element.py
    Class which stores a graph and applies distortions to it.
"""

from __future__ import division

import networkx as nx
import numpy as np

import random
from itertools import compress

__author__ = "Pau Riba, Anjan Dutta"
__email__ = "priba@cvc.uab.cat, adutta@cvc.uab.cat"


class Element:
    def __init__(self, f_name):
        self.el = self.normalize(nx.read_gml(f_name))
        self.label = self.el.graph['class']
        self.displace_node_std = 0
        self.add_node_std = 0
        self.add_edge_prob = 0
        self.rm_edge_prob = 0
        self.edge_connection = 0
        self.max_edge = 0

    def get_label(self):
        return self.label

    def set_distortion(self, displace_node_std, add_node_std, max_edge, add_edge_prob, rm_edge_prob, edge_connection):
        # Node
        self.displace_node_std = displace_node_std
        self.add_node_std = add_node_std

        # Edge
        self.max_edge = max_edge
        self.add_edge_prob = add_edge_prob
        self.rm_edge_prob = rm_edge_prob
        self.edge_connection = edge_connection

    def distort(self):
        g = self.el.copy()

        # Distort nodes
        for k in g.nodes():
            g.node[k]['coord'] = g.node[k]['coord'] + np.random.normal(0, self.displace_node_std, len(g.node[k]['coord']))
            g.node[k]['coord'] = g.node[k]['coord'].tolist()

        # Add edges
        num_edges = np.random.uniform(0,1,self.max_edge)
        num_edges = np.sum(num_edges < self.add_edge_prob)

        for i in range(num_edges):

            s = random.choice(g.nodes())
            if np.random.uniform(0,1,1) < self.edge_connection:
                nodes_g = g.nodes()
                nodes_g.remove(s)
                t = random.choice(nodes_g)
            else:
                t = len(g.nodes())
                g.add_node(t, {'coord': g.node[s]['coord'] + np.random.normal(0, self.add_node_std, len(g.node[s]['coord']))})
            g.add_edge(s, t, {'weight': 1})

        # Remove edges
        rm_edges_prob = np.random.uniform(0, 1, len(g.edges()))
        rm_edges = rm_edges_prob < self.rm_edge_prob
        if np.sum(rm_edges) == len(g.edges()):
            rm_edges[np.argmax(rm_edges)] = False

        g.remove_edges_from(list(compress(g.edges(), rm_edges)))

        # Remove isolated nodes
        g.remove_nodes_from(nx.isolates(g))

        return self.normalize(g)

    def add_nodes(self, d):

        # Create a new graph
        g = nx.Graph()

        # Initialize the nodes given by the prototype
        g.add_nodes_from(self.el.nodes(data=True))

        for s, t, w in self.el.edges_iter(data=True):

            diff_coord = np.array(self.el.node[t]['coord']) - np.array(self.el.node[s]['coord'])

            dist = np.linalg.norm(diff_coord)
            node_to_add = int(dist/d)

            inc = 1/node_to_add

            # Add first node
            g.add_node(len(g.node), {'coord': (inc * diff_coord + self.el.node[s]['coord']).tolist()})
            g.add_edge(s, len(g.node)-1)

            for i in range(2, node_to_add):
                g.add_node(len(g.node), {'coord': (i*inc*diff_coord + self.el.node[s]['coord']).tolist()})
                g.add_edge(len(g.node)-2, len(g.node)-1)

            g.add_edge(len(g.node) - 1, t)
        self.el = self.normalize(g)

    @staticmethod
    def normalize(g):
        coord = [v['coord'] for k, v in g.nodes(data=True)]
        coord = np.array(coord)
        g.graph['mean'] = np.mean(coord, axis=0).tolist()
        g.graph['std'] = np.std(coord, axis=0).tolist()

        for k, v in g.nodes(data=True):
            g.node[k]['coord'] -= np.array(g.graph['mean'])

            # Find all indices of std = 0
            std = [x if x != 0 else 1 for x in g.graph['std']]
            g.node[k]['coord'] = g.node[k]['coord'] / std
            g.node[k]['coord'] = g.node[k]['coord'].tolist()

        return g