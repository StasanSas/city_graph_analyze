import heapq

from my_code.code.algos.statistics.statistic_classes import Statistic


def concat_statistic(statistic: list[Statistic]) -> Statistic:
    if len(statistic) == 0:
        raise ValueError("Дай не пустой массив")

    start = statistic[0]

    for other in statistic[1:]:
        start = concat_pair_statistic(start, other)
    return start

def concat_pair_statistic(self : Statistic, other : Statistic) -> Statistic:
    self.mean_statistic.n += other.mean_statistic.n
    self.mean_statistic.s += other.mean_statistic.s

    #
    per = self.statistic_percentel
    per_o = other.statistic_percentel
    if per.s != per_o.s or per.e != per_o.e or per.step != per_o.step:
        raise Exception('не могу смёржить статистику по общим перцентелям')

    per.n += per_o.n
    for i in range(len(per.array)):
        per.array[i] += per_o.array[i]

    #
    for key in self.statistic_means_for_nodes.d_means_sum:
        if key not in other.statistic_means_for_nodes.d_means_sum:
            raise Exception('Не могу смёржить статистики по среднему для вершин')

        self.statistic_means_for_nodes.d_means_sum[key] += other.statistic_means_for_nodes.d_means_sum[key]
        self.statistic_means_for_nodes.d_means_count[key] += other.statistic_means_for_nodes.d_means_count[key]

    #
    all_per = self.statistic_percentel
    all_per_o = other.statistic_percentel
    if all_per.s != all_per_o.s or all_per.e != all_per_o.e or all_per.step != all_per_o.step:
        raise Exception('Не могу смёржить статистику по перцентелям для вершин')

    for key in self.statistic_percentel_for_nodes.d_arrays:
        if key not in other.statistic_percentel_for_nodes.d_arrays:
            raise Exception('Не могу смёржить статистику по перцентелям для вершин')

        for i in range(len(self.statistic_percentel_for_nodes.d_arrays[key])):
            self.statistic_percentel_for_nodes.d_arrays[key][i] += other.statistic_percentel_for_nodes.d_arrays[key][i]
        self.statistic_percentel_for_nodes.d_n[key] += other.statistic_percentel_for_nodes.d_n[key]

    #
    if self.statistic_max_pairs.amount_elements != other.statistic_max_pairs.amount_elements:
        raise Exception('Нем можем склеить статистику по худшим дистанциям')

    while len(other.statistic_max_pairs.heap) > 0:
        pair_from_other = heapq.heappop(other.statistic_max_pairs.heap)
        heapq.heappush(self.statistic_max_pairs.heap, pair_from_other)
        if len(self.statistic_max_pairs.heap) > self.statistic_max_pairs.amount_elements:
            heapq.heappop(self.statistic_max_pairs.heap)

    return self

if __name__ == "__main__":
    d = {
        "mean" : "True",

        "percentel" : "True",
        "percentel_s" : "0",
        "percentel_e": f"{100}",
        "percentel_step": "1",

        "mean_for_nodes" : "True",

        "percentel_for_nodes" : "True",
        "percentel_for_nodes_k" : "True",
        "max_pairs" : "True",
        "max_pairs_amount" : "4",

        "func_log" : "Tre",
    }
    s = Statistic(d)

    s.process({
        (1, 1): 10, (2, 2) : 20, (3, 3): 30
    })

    s_2 = Statistic(d)
    s_2.process({
        (1, 1): 10, (2, 2): 20, (3, 3): 30
    })

    s_2.process({
        (1, 1): 5, (2, 2): 10, (1, 3): 25
    })
    s = concat_statistic([s, s_2])
    print(s.mean_statistic.get_mean())
    print(s.statistic_percentel.get_percentel(0.5))
    print(s.statistic_means_for_nodes.get_mean(3))
    print(s.statistic_percentel_for_nodes.get_percentel(3, 0.5))
    print(s.statistic_max_pairs.get_pairs())

