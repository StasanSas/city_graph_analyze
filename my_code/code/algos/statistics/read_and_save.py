import json
import os
from dataclasses import asdict

from my_code.code.algos.statistics.dtos import to_dto
from my_code.code.algos.statistics.statistic_classes import Statistic


def save(stat : Statistic, name: str):
    dto = to_dto(stat)
    path = f'../statistic/{name}'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(f'../statistic/{name}', "w") as f:
        json.dump(asdict(dto), f, indent=2, ensure_ascii=False)


def load(name: str):
    path = f'../statistic/{name}'
    with open(path, "r") as f:
        data = json.load(f)

    d_arguments = data["config"]
    obj = Statistic(d_arguments)

    if data.get("mean"):
        obj.mean_statistic.s = data["mean"]["s"]
        obj.mean_statistic.n = data["mean"]["n"]

    if data.get("percentile"):
        p = obj.statistic_percentile
        p.s = data["percentile"]["s"]
        p.e = data["percentile"]["e"]
        p.step = data["percentile"]["step"]
        p.array = data["percentile"]["array"]
        p.n = data["percentile"]["n"]

    if data.get("mean_for_nodes"):
        m = obj.statistic_means_for_nodes
        m.d_means_sum = data["mean_for_nodes"]["d_means_sum"]
        m.d_means_count = data["mean_for_nodes"]["d_means_count"]

    if data.get("percentile_for_nodes"):
        p = obj.statistic_percentile_for_nodes
        p.d_arrays = data["percentile_for_nodes"]["d_arrays"]
        p.d_n = data["percentile_for_nodes"]["d_n"]

    if data.get("max_pairs"):
        m = obj.statistic_max_pairs
        m.heap = data["max_pairs"]["heap"]
        m.amount_elements = data["max_pairs"]["amount_elements"]

    return obj