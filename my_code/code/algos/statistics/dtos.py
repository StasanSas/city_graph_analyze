from dataclasses import dataclass
from typing import List, Dict, Tuple

from my_code.code.algos.statistics.statistic_classes import Statistic


@dataclass
class MeanDTO:
    s: float
    n: int

@dataclass
class PercentileDTO:
    s: int
    e: int
    step: int
    array: List[int]
    n: int

@dataclass
class MeanForNodesDTO:
    d_means_sum: Dict[int, float]
    d_means_count: Dict[int, int]

@dataclass
class PercentileForNodesDTO:
    d_arrays: Dict[int, List[int]]
    d_n: Dict[int, int]
    s: int
    e: int
    step: int

@dataclass
class MaxPairsDTO:
    heap: List[Tuple[float, int, int]]
    amount_elements: int


@dataclass
class StatisticDTO:
    config: Dict[str, str]

    mean: MeanDTO | None = None
    percentile: PercentileDTO | None = None
    mean_for_nodes: MeanForNodesDTO | None = None
    percentile_for_nodes: PercentileForNodesDTO | None = None
    max_pairs: MaxPairsDTO | None = None



def to_dto(stat : Statistic) -> StatisticDTO:
    d = stat.config
    dto = StatisticDTO(config=d)  # можно сохранить d_arguments если нужно

    if "mean" in d:
        dto.mean = MeanDTO(
            s=stat.mean_statistic.s,
            n=stat.mean_statistic.n
        )

    if "percentile" in d:
        p = stat.statistic_percentile
        dto.percentile = PercentileDTO(
            s=p.s,
            e=p.e,
            step=p.step,
            array=p.array,
            n=p.n
        )

    if "mean_for_nodes" in d:
        m = stat.statistic_means_for_nodes
        dto.mean_for_nodes = MeanForNodesDTO(
            d_means_sum=m.d_means_sum,
            d_means_count=m.d_means_count
        )

    if "percentile_for_nodes" in d:
        p = stat.statistic_percentile_for_nodes
        dto.percentile_for_nodes = PercentileForNodesDTO(
            d_arrays=p.d_arrays,
            d_n=p.d_n,
            s=p.s,
            e=p.e,
            step=p.step
        )

    if "max_pairs" in d:
        m = stat.statistic_max_pairs
        dto.max_pairs = MaxPairsDTO(
            heap=m.heap,
            amount_elements=m.amount_elements
        )

    return dto