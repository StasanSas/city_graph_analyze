from old_code.Graphs.Graph import Graph
import networkx as nx


class PublicTransportGraph(Graph):

    def __init__(self):
        super(PublicTransportGraph, self).__init__()
        #self.current_time = datetime.now()
        self.current_time = 720  # минут
        # идея для времени - получать времяс начала суток, так проще
        # пока предлагаю не привязыватьс к конкретному времени

    def add_pedestrian_way(self, nodes):
        prev_node = nodes[0]
        self.graph.add_node(prev_node.ref, coords=(prev_node.lat, prev_node.lon))
        for i in range(1, len(nodes)):
            curr_node = nodes[i]
            self.graph.add_node(curr_node.ref, coords=(curr_node.lat, curr_node.lon))
            dist = self.haversine((prev_node.lat, prev_node.lon), (curr_node.lat, curr_node.lon))
            time = dist / 4500
            self.graph.add_edge(prev_node.ref, curr_node.ref, weight=time)
            prev_node = curr_node

    def add_public_transport_way(self, nodes_and_time):
        # на вход узел (id, широта, долгота) и время
        prev_node = nodes_and_time[0]
        self.graph.add_node(prev_node[0], coords=(prev_node[1], prev_node[2]))
        for i in range(1, len(nodes_and_time)):
            curr_node = nodes_and_time[i]
            self.graph.add_node(curr_node[0], coords=(curr_node[1], curr_node[2]))
            dist = self.haversine((prev_node[1], prev_node[2]), (curr_node[1], curr_node[2]))
            time = dist / 20000 # приблизительная скорость автомобиля в городе
            self.graph.add_edge(prev_node[0], curr_node[0], weight=time)
            prev_node = curr_node

    def get_shortest_route(self, start, end):
        shortest_route = nx.shortest_path(self.graph, start, end, weight='time')
        return shortest_route