from typing import Callable, Any

import datasketches
from datasketches import kll_floats_sketch
from marshmallow.fields import Boolean

class StatisticAbstract:
    def process(self, stat : dict[tuple[int, int], float]) -> None:
        pass

class StatisticMean(StatisticAbstract):
    s : float
    n : int

    def __init__(self):
        self.s = 0
        self.n = 0

    def process(self, stat : dict[tuple[int, int], float]) -> None:
        for key, value in stat.items():
            self.s += value
            self.n += 1

    def get_mean(self) -> float:
        return self.s / self.n


class StatisticPercentel(StatisticAbstract):
    sketch: kll_floats_sketch

    def __init__(self, k):
        self.sketch = datasketches.kll_floats_sketch(k)

    def __getstate__(self):
        return {'sketch_bytes': self.sketch.serialize()}

    def __setstate__(self, state):
        self.sketch = kll_floats_sketch.deserialize(state['sketch_bytes'])

    def process(self, stat: dict[tuple[int, int], float]) -> None:
        for key, value in stat.items():
            self.sketch.update(value)

    def get_percentel(self, rank) -> float:
        return self.sketch.get_quantile(rank)

class StatisticMeansForNodes(StatisticAbstract):
    d_means_sum: dict[int, float]
    d_means_count: dict[int, float]

    def __init__(self):
        self.d_means_sum = {}
        self.d_means_count = {}

    def process(self, stat: dict[tuple[int, int], float]) -> None:
        for key, value in stat.items():
            start, end = key
            if end not in self.d_means_sum:
                self.d_means_sum[end] = 0
                self.d_means_count[end] = 0
            self.d_means_sum[end] += value
            self.d_means_count[end] += value

    def get_mean(self, node_id) -> float:
        return self.d_means_sum[node_id] / self.d_means_count[node_id]


class StatisticPercentelForNodes(StatisticAbstract):
    d_kll_floats_sketch: dict[int, kll_floats_sketch]
    k : int

    def __init__(self, k):
        self.d_kll_floats_sketch = {}
        self.k = k

    def process(self, stat: dict[int, list[float]]) -> None:
        for key, value in stat.items():
            start, end = key
            if end not in self.d_kll_floats_sketch:
                self.d_kll_floats_sketch[end] = datasketches.kll_floats_sketch(self.k)
            self.d_kll_floats_sketch[end].update(value)

    def get_percentel(self, node_id, rank) -> float:
        return self.d_kll_floats_sketch[node_id].get_quantile(rank)

    def __getstate__(self):
        """Сериализация для передачи между процессами"""
        # Сериализуем каждый sketch в байты
        serialized_sketches = {}
        for node_id, sketch in self.d_kll_floats_sketch.items():
            serialized_sketches[node_id] = sketch.serialize()

        # Возвращаем состояние в сериализуемом виде
        state = {
            'k': self.k,
            'serialized_sketches': serialized_sketches
        }
        return state

    def __setstate__(self, state):
        """Десериализация после получения в другом процессе"""
        self.k = state['k']
        self.d_kll_floats_sketch = {}

        # Восстанавливаем каждый sketch из байтов
        for node_id, sketch_bytes in state['serialized_sketches'].items():
            self.d_kll_floats_sketch[node_id] = datasketches.kll_floats_sketch.deserialize(sketch_bytes)


class Statistic(StatisticAbstract):
    mean_statistic : StatisticMean
    statistic_percentel : StatisticPercentel
    statistic_means_for_nodes : StatisticMeansForNodes
    statistic_percentel_for_nodes : StatisticPercentelForNodes

    __process_statistic : Callable[
        [
            dict[tuple[int, int], float]
        ],
        None
    ]

    def __init__(self, d_arguments: dict[str, Any], func : Callable[[float], float] = lambda x : x) -> None:
        self.__func = func
        self.parse_arguments(d_arguments)
        pass



    def process(self, stat: dict[tuple[int, int], float]) -> None:
        for key, value in stat.items():
            stat[key] = self.__func(value)
        self.__process_statistic(stat)

    def get_k(self, k: str):
        try:
            k_num = int(k)
            if k_num <= 0:
                raise ValueError
            return k_num
        except ValueError:
            raise Exception(f'k = {k} имеет неправильное значение')


    def parse_arguments(self, d : dict[str, Any]):
        func_for_process = []
        if "mean" in d and d["mean"]:
            self.mean_statistic = StatisticMean()
            func_for_process.append(self.mean_statistic.process)

        if "percentel" in d and d["percentel"]:
            k = self.get_k(d["percentel_k"]) if "percentel_k" in d else 52_000
            self.statistic_percentel = StatisticPercentel(k)
            func_for_process.append(self.statistic_percentel.process)

        if "mean_for_nodes" in d and d["mean_for_nodes"]:
            self.statistic_means_for_nodes = StatisticMeansForNodes()
            func_for_process.append(self.statistic_means_for_nodes.process)

        if "percentel_for_nodes" in d and d["percentel_for_nodes"]:
            k = self.get_k(d["percentel_for_nodes_k"]) if "percentel_for_nodes_k" in d else 200
            self.statistic_percentel_for_nodes = StatisticPercentelForNodes(k)
            func_for_process.append(self.statistic_percentel_for_nodes.process)
        self.func_for_process = func_for_process


        self.__process_statistic = self.process_stat

    def process_stat(self, stat: dict[tuple[int, int], float]) -> None:
        for func in self.func_for_process:
            func(stat)

    def __add__(self, other_stat):
        self.mean_statistic.n += other_stat.mean_statistic.n
        self.mean_statistic.s += other_stat.mean_statistic.s
        self.statistic_percentel.sketch.merge(other_stat.statistic_percentel.sketch)

        for key in self.statistic_means_for_nodes.d_means_sum:
            if key not in other_stat.statistic_means_for_nodes.d_means_sum:
                raise Exception('не могу смёржить статистики')

            self.statistic_means_for_nodes.d_means_sum[key] += other_stat.statistic_means_for_nodes.d_means_sum[key]

        for key in self.statistic_means_for_nodes.d_means_count:
            if key not in other_stat.statistic_means_for_nodes.d_means_count:
                raise Exception('не могу смёржить статистики')
            self.statistic_means_for_nodes.d_means_count[key] += other_stat.statistic_means_for_nodes.d_means_count[key]
        return self


if __name__ == "__main__":
    d = {
        "mean" : True,

        "percentel" : True,
        "percentel_k" : 100,

        "mean_for_nodes" : True,

        "percentel_for_nodes" : True,
        "percentel_for_nodes_k" : 1000
    }
    s = Statistic(d)

    s.process({
        (1, 1): 10, (2, 2) : 20, (3, 3): 30
    })

    s.process({
        (1, 1): 10, (2, 2): 20, (3, 3): 30
    })

    s.process({
        (1, 1): 5, (2, 2): 10, (3, 3): 15
    })

    print(s.mean_statistic.get_mean())
    print(s.statistic_percentel.get_percentel(0.5))
    print(s.statistic_means_for_nodes.get_mean(2))
    print(s.statistic_percentel_for_nodes.get_percentel(2, 0.5))
