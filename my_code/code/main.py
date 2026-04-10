from random import shuffle

import time

from my_code.code.algos.distance_finders.dijkstra_transport import DijkstraWithTransport
from my_code.code.algos.statistic_agregators.ParallelTransportDijkstraAggregator import \
    ParallelTransportDijkstraAggregator, create_array_same_statistics
from my_code.code.algos.statistic_agregators.SimpleTransportDijkstraAggregator import SimpleTransportDijkstraAggregator
from my_code.code.algos.statistics.concat_statistic import concat_statistic
from my_code.code.algos.statistics.statistic_classes import Statistic
from my_code.code.algos.transport_routes.transport_routes import TransportRoutes
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

    statistics = create_array_same_statistics(4, d)
    aggregator = ParallelTransportDijkstraAggregator(algos, statistics, 4)

    starts = list(g_nk.iterNodes())[:1000]
    shuffle(starts)

    print('Началось')
    s_time = time.time()
    calculated_statistics = aggregator.aggregate_statistic(starts, 100)
    print('Кончелось')
    final_statistic = concat_statistic(calculated_statistics)

    #print(iteration)
    print(time.time() - s_time)
    print(final_statistic.mean_statistic.get_mean())
    print(final_statistic.statistic_percentel.get_percentel(0.5))





