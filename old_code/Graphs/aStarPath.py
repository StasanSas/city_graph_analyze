import networkx as nx
from geopy.distance import geodesic

class aStarPath:

    def __init__(self, graph):
        self.graph = graph

    @staticmethod
    def f_heuristic(a, b):
        return (abs(a[0]-b[0]) + abs(a[1]-b[1]))


    def a_star_path(self, start, end):
        shortest_route = nx.astar_path(G=self.graph.get_graph(), source=start, target=end, heuristic=aStarPath.f_heuristic, weight='weight')
        return shortest_route


'''
class aStarPath:

    def __init__(self, graph):
        self.graph = graph

    @staticmethod
    def f_heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def a_star_path(self, start, end):
        shortest_route = nx.astar_path(G=self.graph.get_graph(), source=start, target=end, heuristic=aStarPath.f_heuristic, weight='weight')
        return shortest_route
'''