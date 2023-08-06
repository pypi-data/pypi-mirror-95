import argparse

from scipy.sparse import lil_matrix
from scipy.sparse.csgraph import depth_first_order
from cached_property import cached_property
import numpy as np

from homcloud.version import __version__
from homcloud.license import add_argument_for_license
from homcloud.pdgm import PDGM
from homcloud.spatial_searcher import SpatialSearcher


def main(args=None):
    args = args or argument_parser().parse_args()
    with PDGM.open(args.input, 0) as pdgm:
        spatial_searcher = SpatialSearcher(
            list(zip(pdgm.birth_indices, pdgm.death_indices)),
            pdgm.births, pdgm.deaths
        )
        pair = spatial_searcher.nearest_pair(args.x, args.y)
        graph = Graph(pdgm, pair[0], pair[1], args.epsilon)


class Graph(object):
    def __init__(self, pdgm, birth_index, death_index, epsilon):
        self.pdgm = pdgm
        self.boundary_map_chunk = pdgm.boundary_map_chunk
        self.index_to_simplex = pdgm.index_to_simplex
        self.birth_index = birth_index
        self.death_index = death_index
        self.epsilon = epsilon

        assert self.dim(self.birth_index) == 0
        assert self.dim(self.death_index) == 1

        self.build_graph()

    def dim(self, i):
        return self.boundary_map_chunk["map"][i][0]

    def index_to_vertex(self, i):
        return self.index_to_simplex[i][0]

    def edge(self, i):
        x, y = self.boundary_map_chunk["map"][i][1]
        return self.index_to_vertex(x), self.index_to_vertex(y)

    def edge_index_pair(self, i):
        return self.boundary_map_chunk["map"][i][1]

    @property
    def num_vertices(self):
        return self.pdgm.num_vertices

    @property
    def index_to_level(self):
        return self.pdgm.index_to_level

    def build_graph(self):
        death = self.index_to_level[self.death_index]
        self.graph = lil_matrix((self.num_vertices, self.num_vertices), dtype=int)
        for i in range(self.death_index):
            if self.index_to_level[i] > death - self.epsilon:
                break
            if self.dim(i) == 1:
                x, y = self.edge(i)
                self.graph[x, y] = 1

    @cached_property
    def birth_component(self):
        return depth_first_order(self.graph, self.index_to_vertex(self.birth_index),
                                 False, False)

    @property
    def elder_component(self):
        x, y = self.edge(self.death_index)
        if np.count_nonzero(self.birth_component == x):
            return depth_first_order(self.graph, y, False, False)
        else:
            return depth_first_order(self.graph, x, False, False)


def argument_parser():
    p = argparse.ArgumentParser(description="Compute maximal volume in PH0")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_argument_for_license(p)
    tp = p.add_argument_group("target")
    tp.add_argument("-x", required=True, type=float, help="birth time of the pair")
    tp.add_argument("-y", required=True, type=float, help="death time of the pair")

    op = p.add_argument_group("output options")
    op.add_argument("-j", "--json-output", help="output in json format")

    cp = p.add_argument_group("computation parameters")
    cp.add_argument("-e", "--epsilon", type=float, default=0.0,
                    help="noise bandwidth (default: 0.0)")

    p.add_argument("input", help="input filename")
    return p


if __name__ == "__main__":
    main()
