import networkit as nk

from my_code.code.algos.transport_routes import TransportRoutes, DataArrival


class DijkstraWithTransport(nk.distance.Dijkstra):
    def __init__(self, g, source : DataArrival, transportRoutes : TransportRoutes = TransportRoutes([]) , speed = 5, store_paths=True,
                 store_nodes_sorted_by_distance=False, target=None):
        super().__init__(g, source.id_node, store_paths, store_nodes_sorted_by_distance, target)
        self.insertion_count = {}  # счетчик вставок для каждой вершины
        self.extraction_count = {}  # счетчик извлечений
        self.start_position = source
        self.transportRoutes = transportRoutes
        self.speed = speed
