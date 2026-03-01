import os
import networkit as nk
import networkx as nx
import numpy as np
import time

from my_code.code.exper.visualize import find_and_visualize_area
from my_code.code.getter_city_data.getter_nk_graph import nx_to_nk



if __name__ == "__main__":
    path = os.path.join("../city_pedestrian_graph", "Kostroma.graphml")
    graph = nx.read_graphml(path)
    g_nk = nx_to_nk(graph)

    statistic_sum = 0
    n = 0
    for source in g_nk.iterNodes():
        dijkstra = nk.distance.Dijkstra(g_nk, source, storePaths=True)

        # 4. Запускаем алгоритм
        dijkstra.run()

        # 5. Получаем расстояния до всех вершин
        distances = dijkstra.getDistances()
        dist_values = np.array(distances)

        # среднее расстояние (игнорируем бесконечности)
        finite_distances = dist_values[dist_values < 100_000]
        mean_distance = np.mean(finite_distances)
        statistic_sum += mean_distance
        n += 1

    print("Среднее расстояние:", statistic_sum / n)


