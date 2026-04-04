import heapq
from typing import Callable, Iterator, Generator

import networkit as nk

from my_code.code.algos.clusterization.Tree import Tree



def get_dijkstra_trees(graph_iterator : Callable[[int], Iterator[tuple[int, float]]], h3_start : list[int], min_size : float, max_size_coef : float = 4 ) \
        -> Generator[dict[int, Tree]]:

    # min_size говорит, что если встретим другое дерево и мы ещё не набрали min_size, то один из деревьев погибает (судя по скору)
    # по центру кластера получаем список id рёбер и вершин, которые принадлежа этому дереву
    max_size = min_size * max_size_coef

    result = {id : Tree() for id in h3_start}

    distances = {} # int (id старта: id вершины): в : float

    parent = {} # по ключу вершины хранится откуда пришли

    pq = [(0.0, id, id) for id in h3_start]


    while pq:
        dist, s, u = heapq.heappop(pq)
        if dist > max_size:
            continue
        if s not in result:
            continue

        # если деревья тут не бывали
        if u not in parent:
            distances[(s, u)] = dist
            parent[u] = s
            result[s].nodes.add(u)
            result[s].sum_distance += dist

            for v, w in graph_iterator(u):
                new_dist = dist + w
                p = (s,v)
                if (p not in distances or new_dist < distances[p]) and new_dist <= max_size:
                    heapq.heappush(pq, (new_dist, s, v))
                if (v in parent and parent[v] != s and new_dist <= max_size):
                    heapq.heappush(pq, (new_dist, s, v))

        elif parent[u] != s and dist <= min_size: # пришли не из текущего дерева и не нарастили массу
            s_other = parent[u]

            curr_tree_score = result[s].get_score()
            was_here_tree_score = result[s_other].get_score()
            for_delete = s_other \
                if curr_tree_score > was_here_tree_score \
                else s

            for node in result[for_delete].nodes:
                del distances[(for_delete, node)]
                del parent[node]
            del result[for_delete]

            if for_delete == s_other:
                heapq.heappush(pq, (dist, s, u))
            if for_delete == s:
                del parent[u]
                heapq.heappush(pq, (distances[(s_other, u)], s_other, u))
        yield result

def get_trees_with_edges(graph_iterator : Callable[[int], Iterator[tuple[int, float]]],
                         trees :dict[int, Tree]) -> dict[int, Tree]:
    for s, tree in trees.items():
        nodes = tree.nodes
        edges = set()
        for u in nodes:
            for neighbor in graph_iterator(u):
                mi = min(u, neighbor[0])
                ma = max(u, neighbor[0])
                w = neighbor[1]
                if (mi, ma, w) not in edges and neighbor[0] in nodes:
                    edges.add((mi, ma, w))
        tree.edges = edges
    return trees


def get_iterator_with_edges(graph_iterator : Callable[[int], Iterator[tuple[int, float]]],
                            h3_start : list[int], min_size : float, max_size_coef : float = 4) \
        -> Generator[dict[int, Tree]]:
    for iteration_trees in get_dijkstra_trees(graph_iterator, h3_start, min_size, max_size_coef):
        yield get_trees_with_edges(graph_iterator, iteration_trees)

def get_big_tree(graph_iterator : Callable[[int], Iterator[tuple[int, float]]],
                            h3_start : list[int], min_size : float, max_size_coef : float = 4) \
        -> dict[int, Tree]:
    r = None
    for iteration_trees in get_dijkstra_trees(graph_iterator, h3_start, min_size, max_size_coef):
        r = iteration_trees
    return get_trees_with_edges(graph_iterator, r)

d_test_graph = {
        1 : [(5,1)],
        2 : [(5,1), (6, 1)],
        3 : [(5,1)],
        4 : [(5,1), (6,1), (13, 20)],
        5 : [(1,1), (2,1), (3,1), (4,1)],
        6 : [(2, 1), (4, 1), (7, 3)],
        7 : [(6, 3), (8, 1)],
        8 : [(7,1), (9,1), (10,1), (12, 1)],
        9 : [(8,1)],
        10 : [(8,1), (11, 1)],
        11 : [(10,1)],
        12 : [(8,1), (13, 5)],
        13 : [(5, 20), (12, 5), (14, 1), (15, 1), (16, 1)],
        14 : [(13,1)],
        15 : [(13,1)],
        16 : [(13,1)],
    }



def getter_neighbors_test(d : dict[int, list[tuple[int, float]]]) -> Callable[[int], Iterator[tuple[int, float]]]:
    return lambda i : iter(d[i]) if i in d else iter(())

if __name__ == '__main__':

    getter_interator = getter_neighbors_test(d_test_graph)
    d_trees = get_dijkstra_trees(getter_interator, [5, 7, 14], 6, 1)

    i = 0
    for iteration in d_trees:
        i+=1
        print(i)
        print("=====================================")
        for k, v in iteration.items():
            print(k)
            print(", ".join([str(v) for v in v.nodes]))
            print()
        print("=====================================")
        print()
