import networkit as nk

from my_code.code.algos.h3_helper.h3_index import H3Index
from my_code.code.cleaning.abstract_cleaner import CleanerGraph


class CleanerConnectedComponents(CleanerGraph):
    def __init__(self, *args, **kwargs):
        super(CleanerConnectedComponents, self).__init__(*args, **kwargs)


    def get_clean_graph(self, graph : nk.Graph, coordinates_data) -> nk.Graph:
        index = H3Index(coordinates_data)

        # Находим компоненты связности
        cc = nk.components.ConnectedComponents(graph)
        cc.run()

        # Получаем список компонент (каждая — список вершин)
        components = cc.getComponents()
        if not components:
            return nk.Graph(0, weighted=graph.isWeighted(), directed=graph.isDirected())

        components = sorted(components, key=lambda x: len(x), reverse=True)
        statistic = list(map(len, components))
        print(statistic)

        # Находим наибольшую компоненту
        largest_component_nodes = max(components, key=len)

        # Создаём подграф с компактными индексами (с нуля)
        new_graph = nk.graphtools.subgraphFromNodes(
            graph,
            list(largest_component_nodes),
        )

        return new_graph