import copy
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager
from random import shuffle
from typing import Callable, Any

from my_code.code.algos.distance_finders.dijkstra_transport import DijkstraWithTransport
from my_code.code.algos.statistic_agregators.SimpleTransportDijkstraAggregator import SimpleTransportDijkstraAggregator
from my_code.code.algos.statistics.concat_statistic import concat_statistic
from my_code.code.algos.statistics.statistic_classes import Statistic
import networkit as nk

from my_code.code.algos.transport_routes.transport_routes import TransportRoutes
from my_code.code.utilite import identity_func


def aggregate_statistic(algos : DijkstraWithTransport, d_arguments: dict[str, str], batch_start: list[int],
                       size_batch: int, result_dict, process_id):
    aggregator = SimpleTransportDijkstraAggregator(algos, d_arguments)
    aggregator.aggregate_statistic(batch_start, size_batch)
    # Сохраняем результат в общий словарь
    result_dict[process_id] = aggregator.statistics

class ParallelTransportDijkstraAggregator:

    def __init__(self, algos : DijkstraWithTransport, d_arguments: dict[str, str], amount_process = 4):
        self.amount_process = amount_process
        self.algos = algos
        self.d_arguments = d_arguments


    def aggregate_statistic(self, starts : list[int], size_batch_in_process = 10) -> Statistic:

        batches = []
        size_batch = int(len(starts) / self.amount_process) + 1
        for i in range(0, len(starts), size_batch):
            batch = starts[i:min(i + size_batch, len(starts))]
            batches.append(batch)

        manager = Manager()
        result_dict = manager.dict()

        with ProcessPoolExecutor(max_workers=self.amount_process) as executor:
            futures = [
                executor.submit(
                    aggregate_statistic,
                    self.algos,
                    self.d_arguments,
                    batch,
                    size_batch_in_process,
                    result_dict,
                    i
                )
                for i, batch in enumerate(batches)
            ]

            for f in as_completed(futures):
                f.result()  # Ждем завершения

        # Восстанавливаем statistics из result_dict
        result = [result_dict[i] for i in range(len(batches))]
        return concat_statistic(result, self.d_arguments)



