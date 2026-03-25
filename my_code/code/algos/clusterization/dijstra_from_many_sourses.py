import heapq

import networkit as nk

from my_code.code.algos.clusterization.Tree import Tree


def get_dijkstra_trees(graph : nk.Graph, h3_start : list[int], min_size : float, max_size_coef : float = 4 ) \
        -> dict[int, Tree]:

    # min_size говорит, что если встретим другое дерево и мы ещё не набрали min_size, то один из деревьев погибает (судя по скору)
    # по центру кластера получаем список id рёбер и вершин, которые принадлежа этому дереву
    max_size = min_size * max_size_coef

    result = {id : Tree() for id in h3_start}

    distances = {id : 0 for id in h3_start} # int (id старта: id вершины): в : float

    parent = {id : id for id in h3_start} # по ключу вершины хранится откуда пришли

    pq = [(0, id, id) for id in h3_start]


    while pq:
        dist, s, u = heapq.heappop(pq)
        center_curr = parent[s]
        if dist > max_size:
            continue
        if center_curr not in result:
            continue

        # если деревья тут не бывали
        if u not in parent:
            distances[u] = dist
            parent[u] = center_curr
            result[center_curr].nodes.add(u)
            result[center_curr].edges.add((s, u))
            result[center_curr].sum_distance = dist

            for v, w in graph.iterNeighborsWeights(u):
                new_dist = dist + w
                if (v not in distances or new_dist < distances[v]) and new_dist <= max_size:
                    distances[v] = new_dist
                    heapq.heappush(pq, (new_dist, u, v))

        elif parent[u] != center_curr and dist < min_size: # пришли не из текущего дерева и не нарастили массу
            center_which_was_here = parent[u]
            curr_tree_score = result[center_curr].get_score()
            was_here_tree_score = result[center_which_was_here].get_score()
            for_delete = center_which_was_here \
                if curr_tree_score > was_here_tree_score \
                else center_curr

            for node in result[for_delete].nodes:
                del distances[node]
                del parent[node]
                del result[node]


    return result