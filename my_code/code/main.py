import os
from random import shuffle

import networkit as nk
import networkx as nx
import numpy as np
import time

from my_code.code.algos.dijkstra_transport import DijkstraWithTransport
from my_code.code.algos.statistics.statistic_classes import Statistic
from my_code.code.algos.transport_routes.transport_routes import TransportRoutes
from my_code.code.exper.visualize import find_and_visualize_area
from my_code.code.getter_city_data.get_transport_routes import get_transport_routes
from my_code.code.getter_city_data.getter_nk_graph import nx_to_nk
from my_code.code.utilite import read_graphml

if __name__ == "__main__":
    path = "time_pedestrian_graph/Kostroma.graphml"
    graph = read_graphml(path)
    g_nk = nx_to_nk(graph)

    start_time_algos = 8 * 60 * 60
    duration = 2 * 60 * 60
    transport_routes = TransportRoutes(get_transport_routes('Kostroma', start_time_algos, duration))

    algos = DijkstraWithTransport(g_nk, start_time_algos, transport_routes)

    d = {
        "mean": True,

        "percentel": True,
        "percentel_k": 1000,

        "mean_for_nodes": True,

        "percentel_for_nodes": True,
        "percentel_for_nodes_k": 52000
    }
    statistic = Statistic(d)


    starts = list(g_nk.iterNodes())
    shuffle(starts)
    s_time = time.time()
    batch_l = 100
    iteration = 0
    print('Началось')
    for i in range(0, len(starts), batch_l):
        batch = starts[i:min(i + batch_l, len(starts))]
        print("Абоба")
        result = algos.run(batch)
        print("Никита")
        statistic.process(result)
        iteration += 1
        print(iteration)
        print((time.time() - s_time) / (iteration * batch_l))
        print(statistic.mean_statistic.get_mean())
        print(statistic.statistic_percentel.get_percentel(0.5))

        print()





