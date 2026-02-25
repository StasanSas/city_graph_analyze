import networkit as nk

class DijkstraWithTransport(nk.distance.Dijkstra):
    def __init__(self, G, source, time = 0, speed = 5, storePaths=True,
                 storeNodesSortedByDistance=False, target=None):
        super().__init__(G, source, storePaths, storeNodesSortedByDistance, target)
        self.insertion_count = {}  # счетчик вставок для каждой вершины
        self.extraction_count = {}  # счетчик извлечений
