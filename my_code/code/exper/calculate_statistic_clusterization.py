import math

import numpy as np
from matplotlib import pyplot as plt

from my_code.code.algos.clusterization.Cluster import Cluster


def calculate_statistic_by_clusters(clusters : list[Cluster]) -> tuple[list[float], list[float]]:
    edges = []
    sizes = []
    for cluster in clusters:
        edges.extend(cluster.distances)
        sizes.append(len(cluster.distances))
    print(len(clusters))
    print(len(edges))
    edges = sorted(edges)
    sizes = sorted(sizes)
    edges_batch_l = int(len(edges) / 10)
    size_batch_l = int(len(sizes) / 10)

    batches_edges = [float(np.mean(edges[i:i + edges_batch_l])) for i in range(0, len(edges), edges_batch_l)]
    batches_sizes = [float(np.mean(sizes[i:i + size_batch_l])) for i in range(0, len(sizes), size_batch_l)]
    print(batches_edges)
    print(batches_sizes)
    return batches_edges, batches_sizes

def draw_plt(list : list[float], title : str, x_str : str, y_str: str):
    plt.figure(figsize=(10, 6))
    plt.hist(list, bins=100, edgecolor='black', alpha=0.7)

    # Явно задаём деления на осях
    x_ticks = range(0, 10, 2)  # От 0 до 160 с шагом 10
    y_ticks = range(
        math.floor(min(list)),
        math.floor(max(list)),
        math.floor(
            (max(list) - min(list))/5
        )
    )  # От 0 до 1000 с шагом 100 (подбери под свои данные)

    plt.xticks(x_ticks, rotation=45)
    plt.yticks(y_ticks)

    plt.xlabel(x_str)
    plt.ylabel(y_str)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.show()
