from random import shuffle

import time

from my_code.code.algos.distance_finders.dijkstra_transport import DijkstraWithTransport
from my_code.code.algos.statistic_agregators.ParallelTransportDijkstraAggregator import \
    ParallelTransportDijkstraAggregator
from my_code.code.algos.statistic_agregators.SimpleTransportDijkstraAggregator import SimpleTransportDijkstraAggregator
from my_code.code.algos.statistics.concat_statistic import concat_statistic
from my_code.code.algos.statistics.read_and_save import save, load
from my_code.code.algos.statistics.statistic_classes import Statistic
from my_code.code.algos.transport_routes.transport_routes import TransportRoutes
from my_code.code.getter_city_data.get_transport_routes import get_transport_routes
from my_code.code.getter_city_data.getter_nk_graph import nx_to_nk
from my_code.code.utilite import read_graphml

if __name__ == "__main__":
    path = "time_pedestrian_graph/Ekaterinburg.graphml"
    graph = read_graphml(path)
    g_nk = nx_to_nk(graph)

    start_time_algos = 9 * 60 * 60
    duration = 2 * 60 * 60
    transport_routes = TransportRoutes(get_transport_routes('Ekaterinburg', start_time_algos, duration))

    algos = DijkstraWithTransport(g_nk, start_time_algos, transport_routes)

    d = {
        "mean": "True",

        "percentile" : "True",
        "percentile_s" : "0",
        "percentile_e": f"{2 * 60 * 60}",
        "percentile_step": f"{2}",

        "mean_for_nodes": "True",

        "max_pairs": "True",
        "max_pairs_amount" : "100"
    }

    aggregator = ParallelTransportDijkstraAggregator(algos, d, 4)

    starts = list(g_nk.iterNodes())[:1000]
    shuffle(starts)

    print('Началось')
    s_time = time.time()
    final_statistic = aggregator.aggregate_statistic(starts, 30)
    save(final_statistic, 'Ну, базовая статистика')
    s = load('Ну, базовая статистика')
    print(s.config)
    print(s.mean_statistic.get_mean())
    print('Кончелось')

    #print(iteration)
    print(time.time() - s_time)
    print(final_statistic.mean_statistic.get_mean())





