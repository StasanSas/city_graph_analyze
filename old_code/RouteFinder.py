import networkx as nx
class RouteFinder:

    @staticmethod
    def get_shortest_route(start_ref, end_ref, graph):
        shortest_route = nx.shortest_path(graph, start_ref, end_ref, weight='weight')
        return shortest_route

# можно по разным парамтерам строить путь - например кратчайший поь времени