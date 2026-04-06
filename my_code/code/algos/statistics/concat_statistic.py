from my_code.code.algos.statistics.statistic_classes import Statistic


def concat_statistic(statistic: list[Statistic]) -> Statistic:
    if len(statistic) == 0:
        raise ValueError("Дай не пустой массив")

    start = statistic[0]

    for stat in statistic[1:]:
        start += stat
    return start
