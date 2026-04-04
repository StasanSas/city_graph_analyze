import heapq
from datetime import time

import networkit as nk
import networkx as nx

from my_code.code.algos.statistics.statistic_classes import Statistic
from my_code.code.algos.transport_routes.transport_routes import TransportRoutes, DataArrival, TransportRoute
from my_code.code.getter_city_data.getter_nk_graph import nx_to_nk_with_extra, nx_to_nk
from my_code.code.utilite import getter_neighbors, time_to_seconds


class DijkstraWithTransport():
    def __init__(self, g : nk.Graph, start_time : float, transport_routes : TransportRoutes = TransportRoutes([])):
        # g ПЕШЕХОДНЫЙ граф с рёбрами, содержащими информацию о ВРЕМЕНИ движения между вершинами
        # start_time время отправления пешехода из своей начальной точки
        # можно было добавить как аргумент в run, но мы делаем на основе этого времени предобработку transportRoutes
        # TransportRoutes  - структура, необходимая для обработки маршрутов общественного транспорта
        # Её нужно создавать с умом, чтобы была связана с графом g.
        self.g = g
        self.start_time = start_time
        self.transport_routes = transport_routes
        pass


    # передаём словарь
    def run(self, starts : list[int]) -> dict[tuple[int, int], float]:
        # min_size говорит, что если встретим другое дерево и мы ещё не набрали min_size, то один из деревьев погибает (судя по скору)
        # по центру кластера получаем список id рёбер и вершин, которые принадлежа этому дереву

        times = {}  # int (id старта: id вершины): в : float

        for s in starts:
            pq = [(0.0, s)]

            while pq:
                time, u = heapq.heappop(pq)
                if (s, u) in times:
                    continue

                times[(s, u)] = time

                for v, w in self.g.iterNeighborsWeights(u):
                    new_time = time + w
                    p = (s, v)
                    if p not in times:
                        heapq.heappush(pq, (new_time, v))

                if self.transport_routes.is_stop(u):
                    next_data_arrival = self.transport_routes.get_nearest_routes_for_stop(DataArrival(u, time))
                    for data_arrival in next_data_arrival:
                        heapq.heappush(pq, (data_arrival.arrival_time, data_arrival.id_node))
        return times

#         5
#  1 ------------2
#  |             |
#  |5            |10          1 -> 4  в 1 минуту и прибывает в 6 минуту
#  |  4      8   |            4 -> 7  в 6 минуту отправляется и в 11 минуту прибывает
#  3------4------5
#  |             |
#  |1            |2
#  |             |
#  6             7
#                | 4
#                8
#
if __name__ == "__main__":
    path = 'test.graphml'
    nx_graph = nx.read_graphml(path)
    graph_nk = nx_to_nk(nx_graph)

    d_1 = {}
    s_1__1_00 = DataArrival(1, time_to_seconds(time(0, 1, 0)))

    s_4__6_00 = DataArrival(4, time_to_seconds(time(0, 6, 00)))
    d_1[s_1__1_00] = s_4__6_00

    s_7__11_00 = DataArrival(7, time_to_seconds(time(0, 11, 00)))
    d_1[s_4__6_00] = s_7__11_00

    route_1 = TransportRoute(1, "Чикибамбоники - Рыбинск", d_1)

    routes = TransportRoutes([route_1])
    algos = DijkstraWithTransport(graph_nk, 0.0, routes)
    result = algos.run([1])
    for key, value in result.items():
        print(f'{key}: {value}')

