from multiprocessing import heap
from typing import Callable, Any
import heapq
import datasketches
from datasketches import kll_floats_sketch
from marshmallow.fields import Boolean
from math import log

def get_func(d: dict[str, str]) -> Callable[[int, int, float], float]:
    d_func = {
        "func_log" : lambda _0, _1, x : log(x)
    }
    for k, v in d_func.items():
        if k in d and d[k].upper() == "TRUE":
            return v
    return lambda _0, _1, x: x

def get_int(string: str, d: dict[str, str]):
    try:
        if string not in d:
            raise Exception(f'Нет в словаре необходимого ключа = {string}')
        num = int(d[string])
        if num < 0:
            raise Exception(f'{string} = {d[string]} должно быть больше 0 либо равно')
        return num
    except ValueError:
        raise Exception(f'{string} = {d[string]} не является int')

class StatisticAbstract:
    def process(self, stat : dict[tuple[int, int], float]) -> None:
        pass

class StatisticMean(StatisticAbstract):
    s : float
    n : int

    def __init__(self, d : dict[str, str]):
        self.s = 0
        self.n = 0

    def process(self, stat : dict[tuple[int, int], float]) -> None:
        for key, value in stat.items():
            self.s += value
            self.n += 1

    def get_mean(self) -> float:
        return self.s / self.n


class StatisticPercentel(StatisticAbstract):
    s : int
    e : int
    step : int
    array : list[int]
    n : int

    def __init__(self, d : dict[str, str]):
        self.s = get_int("percentel_s", d)
        self.e = get_int("percentel_e", d)
        self.step = get_int("percentel_step", d)
        end_range = self.e + self.step if (self.e - self.s) % self.step == 0 else self.e + (2 * self.step)
        self.array = [0 for i in range(self.s - self.step, end_range, self.step)]
        self.n = 0



    def get_index_for_value(self, v) -> int:
        pos = int(((v - self.s) // self.step) + 1)
        if pos <= 0:
            return 0
        if len(self.array) - 1 <= pos:
            return len(self.array) - 1
        return pos


    def process(self, stat: dict[tuple[int, int], float]) -> None:
        for key, value in stat.items():
            pos = self.get_index_for_value(value)
            self.array[pos] += 1
            self.n += 1

    def index_pos(self, rank):
        return int((self.n * rank + 1) // 1)

    def get_percentel(self, rank) -> float:
        target = self.index_pos(rank)

        mid_st = (float(self.step) / 2)
        if self.array[0] > target:
            return -2.0
        if self.array[0] + self.array[1] > target:
            return self.s + mid_st

        c = self.array[0] + self.array[1]
        i_last = 1 if self.array[1] > 0 else -1
        c_last = 0

        for i in range(2, len(self.array) - 1):
            if self.array[i] == 0:
                continue
            c += self.array[i]
            if c >= target:
                curr_v = float(self.s + (i - 1) * self.step + mid_st)
                if i_last == -1 or c > target:
                    return curr_v
                last_v = float(self.s + (i_last - 1) * self.step + mid_st)

                dist_last = float(target - c_last)
                dist_cur = float(c - target)
                return last_v + (curr_v - last_v) * (dist_last / (dist_cur + dist_last))
            i_last = i
            c_last = c
        return -1.0

    def get_array(self):
        return self.array.copy()

class StatisticMeansForNodes(StatisticAbstract):
    d_means_sum: dict[int, float]
    d_means_count: dict[int, int]

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
            self.d_means_count[end] += 1

    def get_mean(self, node_id) -> float:
        return self.d_means_sum[node_id] / self.d_means_count[node_id]


class StatisticPercentelForNodes(StatisticAbstract):
    d_arrays: dict[int, list[int]]
    d_n: dict[int, int]


    def __init__(self, d : dict[str, str]):
        self.s = get_int("percentel_s", d)
        self.e = get_int("percentel_e", d)
        self.step = get_int("percentel_step", d)
        self.end_range = self.e + self.step if (self.e - self.s) % self.step == 0 else self.e + (2 * self.step)
        self.len = (self.end_range - (self.s - self.step)) // self.step
        self.d_arrays = {}
        self.d_n = {}


    def get_index_for_value(self, v) -> int:
        pos = int(((v - self.s) // self.step) + 1)
        if pos <= 0:
            return 0
        if self.len - 1 <= pos:
            return self.len - 1
        return pos

    def process(self, stat: dict[tuple[int, int], float]) -> None:
        for key, value in stat.items():
            start, end = key
            if end not in self.d_arrays:
                self.d_arrays[end] = [0 for i in range(self.s - self.step, self.end_range, self.step)]
                self.d_n[end] = 0
            pos = self.get_index_for_value(value)
            self.d_arrays[end][pos] += 1
            self.d_n[end] += 1

    def index_pos(self, node_id, rank):
        return int((
                           (self.d_n[node_id] * rank) + 1
                   )// 1)

    def get_percentel(self, node_id, rank) -> float:
        target = self.index_pos(node_id, rank)
        array = self.d_arrays[node_id]

        mid_st = (float(self.step) / 2)
        if array[0] > target:
            return -2.0
        if array[0] + array[1] > target:
            return self.s + mid_st

        c = array[0] + array[1]
        i_last = 1 if array[1] > 0 else -1
        c_last = 0

        for i in range(2, len(array) - 1):
            if array[i] == 0:
                continue
            c += array[i]
            if c >= target:
                curr_v = float(self.s + (i - 1) * self.step + mid_st)
                if i_last == -1 or c > target:
                    return curr_v
                last_v = float(self.s + (i_last - 1) * self.step + mid_st)

                dist_last = float(target - c_last)
                dist_cur = float(c - target)
                return last_v + (curr_v - last_v) * (dist_last / (dist_cur + dist_last))
            i_last = i
            c_last = c
        return -1.0


class StatisticMaxPairs(StatisticAbstract):
    heap : list[tuple[float, int, int]]
    amount_elements : int

    def __init__(self, d : dict[str, str]):
        self.heap = []
        self.amount_elements = get_int("max_pairs_amount", d)

    def process(self, stat: dict[tuple[int, int], float]) -> None:
        for key, value in stat.items():
            start, end = key
            heapq.heappush(self.heap, (value, start, end))
            if len(self.heap) > self.amount_elements:
                heapq.heappop(self.heap)

    def get_pairs(self) -> list[tuple[float, int, int]]:
        return sorted(self.heap, reverse=True)



class Statistic(StatisticAbstract):
    mean_statistic : StatisticMean
    statistic_percentel : StatisticPercentel
    statistic_means_for_nodes : StatisticMeansForNodes
    statistic_percentel_for_nodes : StatisticPercentelForNodes
    statistic_max_pairs : StatisticMaxPairs

    __process_statistic : Callable[
        [
            dict[tuple[int, int], float]
        ],
        None
    ]

    def __init__(self, d_arguments: dict[str, Any]) -> None:
        self.__func = get_func(d_arguments)
        self.parse_arguments(d_arguments)
        pass


    def process(self, stat: dict[tuple[int, int], float]) -> None:
        for key, value in stat.items():
            s, e = key
            stat[key] = self.__func(s, e, value)
        self.__process_statistic(stat)


    def parse_arguments(self, d : dict[str, str]):
        func_for_process = []
        if "mean" in d and d["mean"].upper() == "TRUE":
            self.mean_statistic = StatisticMean(d)
            func_for_process.append(self.mean_statistic.process)

        if "percentel" in d and d["percentel"].upper() == "TRUE":
            self.statistic_percentel = StatisticPercentel(d)
            func_for_process.append(self.statistic_percentel.process)

        if "mean_for_nodes" in d and d["mean_for_nodes"].upper() == "TRUE":
            self.statistic_means_for_nodes = StatisticMeansForNodes()
            func_for_process.append(self.statistic_means_for_nodes.process)

        if "percentel_for_nodes" in d and d["percentel_for_nodes"].upper() == "TRUE":
            self.statistic_percentel_for_nodes = StatisticPercentelForNodes(d)
            func_for_process.append(self.statistic_percentel_for_nodes.process)

        if "max_pairs" in d and d["max_pairs"].upper() == "TRUE":
            self.statistic_max_pairs = StatisticMaxPairs(d)
            func_for_process.append(self.statistic_max_pairs.process)

        self.func_for_process = func_for_process

        self.__process_statistic = self.process_stat

    def process_stat(self, stat: dict[tuple[int, int], float]) -> None:
        for func in self.func_for_process:
            func(stat)
