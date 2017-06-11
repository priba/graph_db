import networkx as nx


class Element:
    def __init__(self, f_name):
        self.el = nx.read_gml(f_name)

    def distort(self):
        nx.write_gml(g, f_name)