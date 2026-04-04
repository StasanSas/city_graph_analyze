from typing import Callable, Any

import datasketches
from datasketches import kll_floats_sketch
from marshmallow.fields import Boolean

class StatisticAbstract:
    def process(self, stat : dict[tuple[int, int], float]) -> None:
        pass

class StatisticMean(StatisticAbstract):
    __s : float
    __n : int

    def __init__(self):
        self.__s = 0
        self.__n = 0

    def process(self, stat : dict[tuple[int, int], float]) -> None:
        for key, value in stat.items():
            self.__s += value
            self.__n += 1

    def get_mean(self) -> float:
        return self.__s / self.__n


class StatisticPercentel(StatisticAbstract):
    __sketch: kll_floats_sketch

    def __init__(self, k):
        self.__sketch = datasketches.kll_floats_sketch(k)

    def process(self, stat: dict[tuple[int, int], float]) -> None:
        for key, value in stat.items():
            self.__sketch.update(value)

    def get_percentel(self, rank) -> float:
        return self.__sketch.get_quantile(rank)

class StatisticMeansForNodes(StatisticAbstract):
    __d_means_sum: dict[int, float]
    __d_means_count: dict[int, float]

    def __init__(self):
        self.__d_means_sum = {}
        self.__d_means_count = {}

    def process(self, stat: dict[tuple[int, int], float]) -> None:
        for key, value in stat.items():
            start, end = key
            if end not in self.__d_means_sum:
                self.__d_means_sum[end] = 0
                self.__d_means_count[end] = 0
            self.__d_means_sum[end] += value
            self.__d_means_count[end] += value

    def get_mean(self, node_id) -> float:
        return self.__d_means_sum[node_id] / self.__d_means_count[node_id]


class StatisticPercentelForNodes(StatisticAbstract):
    __d_kll_floats_sketch: dict[int, kll_floats_sketch]
    __k : int

    def __init__(self, k):
        self.__d_kll_floats_sketch = {}
        self.__k = k

    def process(self, stat: dict[int, list[float]]) -> None:
        for key, value in stat.items():
            start, end = key
            if end not in self.__d_kll_floats_sketch:
                self.__d_kll_floats_sketch[end] = datasketches.kll_floats_sketch(self.__k)
            self.__d_kll_floats_sketch[end].update(value)

    def get_percentel(self, node_id, rank) -> float:
        return self.__d_kll_floats_sketch[node_id].get_quantile(rank)

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
        l_true = ["true", "True", True]
        if "mean" in d and d["mean"] in l_true:
            self.mean_statistic = StatisticMean()
            func_for_process.append(self.mean_statistic.process)

        if "percentel" in d and d["percentel"] in l_true:
            k = self.get_k(d["percentel_k"]) if "percentel_k" in d else 52_000
            self.statistic_percentel = StatisticPercentel(k)
            func_for_process.append(self.statistic_percentel.process)

        if "mean_for_nodes" in d and d["mean_for_nodes"] in l_true:
            self.statistic_means_for_nodes = StatisticMeansForNodes()
            func_for_process.append(self.statistic_means_for_nodes.process)

        if "percentel_for_nodes" in d and d["percentel_for_nodes"] in l_true:
            k = self.get_k(d["percentel_for_nodes_k"]) if "percentel_for_nodes_k" in d else 200
            self.statistic_percentel_for_nodes = StatisticPercentelForNodes(k)
            func_for_process.append(self.statistic_percentel_for_nodes.process)

        def process_stat(stat : dict[tuple[int, int], float]) -> None:
            for func in func_for_process:
                func(stat)

        self.__process_statistic = process_stat

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
