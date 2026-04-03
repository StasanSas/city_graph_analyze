import os

import networkx as nx

from my_code.code.cleaning.cleaner_one_connected_component import ConverterConnectedComponents
from my_code.code.exper.visualize import find_and_visualize_area
from my_code.code.getter_city_data.getter_nk_graph import nx_to_nk_with_extra, nk_to_nx


def compare_nx_graphs(G1: nx.Graph, G2: nx.Graph, check_attributes: bool = True) -> bool:
    """
    Сравнивает два NetworkX графа
    """
    # Базовая проверка структуры
    if G1.number_of_nodes() != G2.number_of_nodes():
        print(f"Разное количество вершин: {G1.number_of_nodes()} vs {G2.number_of_nodes()}")
        return False
    print(4)
    if G1.number_of_edges() != G2.number_of_edges():
        print(f"Разное количество рёбер: {G1.number_of_edges()} vs {G2.number_of_edges()}")
        return False
    print(5)
    degrees1 = sorted([d for n, d in G1.degree()])
    degrees2 = sorted([d for n, d in G2.degree()])

    if degrees1 != degrees2:
        return False
    print(6)
    if check_attributes:
        # Проверка атрибутов вершин
        for node in G1.nodes():
            if node not in G2:
                print(f"Вершина {node} отсутствует во втором графе")
                return False
            if G1.nodes[node] != G2.nodes[node]:
                print(f"Разные атрибуты для вершины {node}: {G1.nodes[node]} vs {G2.nodes[node]}")
                return False
        print(7)
        # Проверка атрибутов рёбер
        for u, v in G1.edges():
            if not G2.has_edge(u, v):
                print(f"Ребро ({u}, {v}) отсутствует во втором графе")
                return False
            if G1.edges[u, v] != G2.edges[u, v]:
                print(f"Разные атрибуты для ребра ({u}, {v}): {G1.edges[u, v]} vs {G2.edges[u, v]}")
                return False

    print("Графы полностью идентичны")
    return True

path_input = "Kostroma.graphml"
path_output = "one_component/Kostroma.graphml"
cleaner = ConverterConnectedComponents()

cleaner.run(path_input, path_output)

#graph = nx.read_graphml("../city_cleaned_graphs/" + path_output)
#graph = nx.read_graphml("C:\\Users\\stanislav.ivanov\\Desktop\\city_graph_analyze\\my_code\\city_pedestrian_graph\\Kostroma.graphml")


print(3)


