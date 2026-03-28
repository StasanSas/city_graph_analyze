import heapq
from typing import Callable, Iterator

from my_code.code.algos.clusterization.Cluster import Cluster
from my_code.code.algos.clusterization.Tree import Tree
from my_code.code.algos.clusterization.dijstra_from_many_sourses import d_test_graph, getter_neighbors_test


def get_best_cluster(graph_iterator: Callable[[int], Iterator[tuple[int, float]]], tree : Tree, max_size: float) -> Cluster:
    max_score = None
    res = None
    for u in tree.nodes:
        cluster = get_cluster(graph_iterator, tree, u, max_size)
        if max_score is None or max_score < cluster.get_score():
            max_score = cluster.get_score()
            res = cluster
    return res

def get_cluster(graph_iterator: Callable[[int], Iterator[tuple[int, float]]], tree : Tree, start : int, max_size: float) -> Cluster:

    result = Cluster()
    if start not in tree.nodes:
        return result
    result.center = start
    distances = {} # int (id старта: id вершины): в : float

    pq = [(0, start, start)]

    while pq:
        dist, s, u = heapq.heappop(pq)
        if dist > max_size:
            continue

        # если деревья тут не бывали
        if u not in distances:
            distances[(s, u)] = dist
            result.nodes.add(u)
            result.distances.add(dist)

            for v, w in graph_iterator(u):
                if v not in tree.nodes:
                    continue
                new_dist = dist + w
                p = (s, v)
                if (p not in distances or new_dist < distances[p]) and new_dist <= max_size:
                    heapq.heappush(pq, (new_dist, s, v))
    return result


if __name__ == '__main__':

    tree = Tree()
    getter_interator = getter_neighbors_test(d_test_graph)
    tree.nodes = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}
    cluster = get_best_cluster(getter_interator, tree, 1)


    print(cluster.center)
    print(", ".join([str(v) for v in cluster.nodes]))
    print()
