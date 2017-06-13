#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    to_image.py
    Reads the graphs saved into a folder and plots into a png.
"""

import networkx as nx
from Plotter import plot_graph

import os
import glob

import argparse

__author__ = "Pau Riba, Anjan Dutta"
__email__ = "priba@cvc.uab.cat, adutta@cvc.uab.cat"

parser = argparse.ArgumentParser(description='Process prototype folder.')
parser.add_argument('--dir', help='prototype folder', default='./Letters/')

args = parser.parse_args()

if __name__ == '__main__':
    files = glob.glob(args.dir + '*.gml')
    for f in files:
        g = nx.read_gml(f)
        base = os.path.splitext(f)[0]
        plot_graph(g, save_path=base+'.png')

