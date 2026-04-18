from my_code.code.convertors_graph.abstract_cleaner import ConverterGraph
import networkit as nk

class ConverterDistanceInTimes(ConverterGraph):
    def __init__(self, speed_meters_in_second : float = 1.4):
        if speed_meters_in_second <= 0.0001:
            raise ValueError("Ты чо дебил чтоле")
        self.speed = speed_meters_in_second


    def get_converted_graph(self, graph : nk.Graph, coordinates_data : dict[int, dict[str, float]]) -> nk.Graph:
        new_g = nk.Graph(graph.numberOfNodes(), weighted=True, directed=graph.isDirected())

        for u, v in graph.iterEdges():
            w = graph.weight(u, v) / self.speed
            new_g.addEdge(u, v, w)
        return new_g
