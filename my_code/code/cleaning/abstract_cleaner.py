import os

import networkx as nx
import networkit as nk

from my_code.code.getter_city_data.getter_nk_graph import nx_to_nk_with_extra, nk_to_nx
from my_code.code.utilite import read_graphml, write_graphml


class ConverterGraph():
    def __init__(self, *args, **kwargs):
        super(ConverterGraph, self).__init__(*args, **kwargs)

    def get_converted_graph_nx(self, graph : nx.Graph) -> nx.Graph:
        """Очистка графа nx"""
        graph_nk, coordinates_data = nx_to_nk_with_extra(graph)
        new_nk_graph = self.get_converted_graph(graph_nk, coordinates_data)
        return nk_to_nx(new_nk_graph, coordinates_data)

    def get_converted_graph(self, graph : nk.Graph, coordinates_data : dict[int, dict[str, float]]) -> nk.Graph:
        """Очистка графа nk"""
        pass


    def run(self, part_path_input, part_path_output):
        graph = read_graphml(part_path_input)
        new_graph = self.get_converted_graph_nx(graph)
        # Перенумеровываем вершины с 0
        mapping = {old_label: new_label for new_label, old_label in enumerate(new_graph.nodes())}
        new_graph = nx.relabel_nodes(new_graph, mapping, copy=True)
        write_graphml(new_graph, part_path_output)

