import math
import networkx as nx
from old_code.Graphs.aStarPath import aStarPath


class Graph:
    def __init__(self):
        self.graph = nx.Graph()
        self.a = []

    def haversine(self, point_a, point_b):
        # Радиус Земли в километрах
        R = 6371.0

        # Преобразуем широту и долготу из градусов в радианы
        lat_a, lon_a = math.radians(point_a[0]), math.radians(point_a[1])
        lat_b, lon_b = math.radians(point_b[0]), math.radians(point_b[1])

        # Разница координат
        dlat = lat_b - lat_a
        dlon = lon_b - lon_a

        # Формула haversine
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat_a) * math.cos(lat_b) * math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))

        # Расстояние в метрах
        distance = R * c
        return distance * 1000

    # добавляет какой-то один путь - и узлы, и ребра между ними для этого пути
    def add_way(self, nodes):
        prev_node = nodes[0]
        self.graph.add_node((prev_node.lat, prev_node.lon))
        for i in range(1, len(nodes)):
            curr_node = nodes[i]
            self.graph.add_node((curr_node.lat, curr_node.lon))
            dist = self.haversine((prev_node.lat, prev_node.lon), (curr_node.lat, curr_node.lon))
            #self.a.append(dist)
            self.graph.add_edge((prev_node.lat, prev_node.lon), (curr_node.lat, curr_node.lon), weight=dist)
            prev_node = curr_node

    def get_graph(self):
        #print(self.get_detailed_statistics())
        return self.graph

    def get_list_of_nodes_coords(self, list_of_nodes):
        nodes_coords = [self.graph.nodes[node] for node in list_of_nodes]
        return nodes_coords

    def get_node_coords(self, node):
        return node

    def get_sorted_nodes(self):
        sorted_nodes = sorted(self.graph.nodes(), key=lambda node: (node[0], node[1]))
        return sorted_nodes

    def get_shortest_route(self, start, end):
        shortest_route = nx.shortest_path(self.graph, start, end, weight='weight', method='dijkstra')
        a_star = aStarPath(self)
        shortest_route = a_star.a_star_path(start, end)
        return shortest_route

    def get_detailed_statistics(self):
        """Детальная статистика по длинам рёбер"""

        sorted_lengths = sorted(self.a)
        n = len(sorted_lengths)

        return {
            'count': n,
            'min': sorted_lengths[0],
            'max': sorted_lengths[-1],
            'mean': sum(sorted_lengths) / n,
            'median': sorted_lengths[n // 2] if n % 2 == 1 else
            (sorted_lengths[n // 2 - 1] + sorted_lengths[n // 2]) / 2,
            'q1': sorted_lengths[n // 4],
            'q3': sorted_lengths[3 * n // 4],
            'total': sum(sorted_lengths),
        }