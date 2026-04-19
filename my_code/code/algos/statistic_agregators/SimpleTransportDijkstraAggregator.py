import time
from random import shuffle
from concurrent.futures import ProcessPoolExecutor
from my_code.code.algos.distance_finders.dijkstra_transport import DijkstraWithTransport
from my_code.code.algos.statistics.statistic_classes import Statistic
import networkit as nk

from my_code.code.algos.transport_routes.transport_routes import TransportRoutes


class SimpleTransportDijkstraAggregator:
    algos : DijkstraWithTransport

    def __init__(self, algos : DijkstraWithTransport, d_arguments: dict[str, str]):
        self.statistics = Statistic(d_arguments)
        self.algos = algos


    def aggregate_statistic(self, starts : list[int], size_batch : int = 100):
        s_time = time.time()
        for i in range(0, len(starts), size_batch):
            batch = starts[i:min(i + size_batch, len(starts))]
            result = self.algos.run(batch)
            self.statistics.process(result)
            print(i)
            print((time.time() - s_time) / ((i + 1) * size_batch))
            print()
        return self.statistics

