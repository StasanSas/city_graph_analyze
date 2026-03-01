import os
from abc import ABC, abstractmethod

import networkx as nx


class CleanerGraph(ABC):
    def __init__(self, *args, **kwargs):
        super(CleanerGraph, self).__init__(*args, **kwargs)

    @abstractmethod
    def get_clean_graph(self, graph : nx.Graph) -> nx.Graph:
        """Очистка графа"""
        pass


    def read_graphml(self, part_path : str) -> nx.Graph:
        path = os.path.join("../../city_pedestrian_graph", part_path)
        if os.path.exists(path):
            return nx.read_graphml(path)
        else:
            path = os.path.join("../../city_cleaned_graphs", part_path)
            return nx.read_graphml(path)


    def write_graphml(self, graph : nx.Graph, part_path : str) -> None:
        base_path = "../../city_cleaned_graphs"
        parts_path = part_path.split("/")
        if len(parts_path) != 2:
            raise Exception("Дай папку")
        if os.path.isdir(os.path.join(base_path, parts_path[0])):
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
        new_graph = self.get_clean_graph(graph)
        self.write_graphml(new_graph, part_path_output)

