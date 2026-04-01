import networkit as nk

from my_code.code.algos.transport_routes.transport_routes import TransportRoutes, DataArrival


class DijkstraWithTransport(nk.distance.Dijkstra):
    def __init__(self, g, source : DataArrival, transportRoutes : TransportRoutes = TransportRoutes([]) , speed = 5, store_paths=True,
                 store_nodes_sorted_by_distance=False, target=None):
        super().__init__(g, source.id_node, store_paths, store_nodes_sorted_by_distance, target)
        self.insertion_count = {}  # счетчик вставок для каждой вершины
        self.extraction_count = {}  # счетчик извлечений
        self.start_position = source
        self.transportRoutes = transportRoutes
        self.speed = speed



class HybridDijkstraWithMultiplier(nk.distance.Dijkstra):
    def __init__(self, G, source, multiplier=1.0, **kwargs):
        super().__init__(G, source, **kwargs)
        self.multiplier = multiplier

        # СОЗДАЕМ НОВЫЙ ГРАФ с измененными весами
        # Это самый надежный способ использовать C++ код
        self.modified_G = self.create_modified_graph(G, multiplier)

    def create_modified_graph(self, G, multiplier):
        """Создает копию графа с умноженными весами"""
        n = G.upperNodeIdBound()
        new_G = nk.Graph(n, weighted=True, directed=G.isDirected())

        # Копируем все ребра с новыми весами
        for u in range(n):
            for (v, w) in G.iterNeighbors(u):
                if u < v or G.isDirected():  # избегаем дублирования
                    new_G.addEdge(u, v, w * multiplier)

        return new_G

    def run(self):
        # Заменяем граф на модифицированный и запускаем родительский run
        original_G = self._G
        self._G = self.modified_G

        # Вызываем родительский run (весь на C++!)
        result = super().run()

        # Возвращаем исходный граф (чтобы не сломать другие алгоритмы)
        self._G = original_G

        return result

    # Можно даже не переопределять explore!