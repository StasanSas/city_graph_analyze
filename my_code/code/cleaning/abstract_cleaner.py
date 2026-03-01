import os

import networkx as nx
import networkit as nk

from my_code.code.getter_city_data.getter_nk_graph import nx_to_nk_with_extra, nk_to_nx


class CleanerGraph():
    def __init__(self, *args, **kwargs):
        super(CleanerGraph, self).__init__(*args, **kwargs)

    def get_clean_graph_nx(self, graph : nx.Graph) -> nx.Graph:
        """Очистка графа nx"""
        graph_nk, coordinates_data = nx_to_nk_with_extra(graph)
        new_nk_graph = self.get_clean_graph(graph_nk)
        return nk_to_nx(new_nk_graph, coordinates_data)

    def get_clean_graph(self, graph : nk.Graph) -> nk.Graph:
        """Очистка графа nk"""
        pass


    def read_graphml(self, part_path : str) -> nx.Graph:
        path = os.path.join("../city_pedestrian_graph", part_path)
        print(os.path.abspath(path))
        if os.path.exists(path):
            return nx.read_graphml(path)
        else:
            path = os.path.join("../city_cleaned_graphs", part_path)
            return nx.read_graphml(path)


    def write_graphml(self, graph : nx.Graph, part_path : str) -> None:
        base_path = "../city_cleaned_graphs"
        parts_path = part_path.split("/")
        if len(parts_path) != 2:
            raise Exception("Дай папку")
        if not os.path.isdir(os.path.join(base_path, parts_path[0])):
            raise Exception("Нет такой папки")
        path = os.path.join(base_path, part_path)
        nx.write_graphml(
        graph,
        path,
        encoding="utf-8",
        prettyprint=True
    )


    def run(self, part_path_input, part_path_output):
        graph = self.read_graphml(part_path_input)
        new_graph = self.get_clean_graph_nx(graph)
        # Перенумеровываем вершины с 0
        mapping = {old_label: new_label for new_label, old_label in enumerate(new_graph.nodes())}
        new_graph = nx.relabel_nodes(new_graph, mapping, copy=True)
        self.write_graphml(new_graph, part_path_output)

