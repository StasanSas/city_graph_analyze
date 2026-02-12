"""
Transit-aware clustered shortest path
- Pedestrian graph: undirected edges (walk times)
- Transit routes: directed sequences of stops with travel times and schedules
- Clusterization: Dijkstra-limited around stops (parameter k)
- Precompute: all-pairs distances inside each cluster
- Compressed graph: boundary vertices + stops, edges weighted by intra-cluster distances
- Query: modified Dijkstra in compressed graph with boarding/waiting logic

Примечание по расписаниям:
  route.arrivals[stop_index] = [t0, t1, t2, ...]  # times for successive trips
  length of arrivals[stop_index] должна совпадать для всех stop_index одного route,
  индекс trip_idx относится к одному и тому же физическому рейсу/экземпляру.
"""

import heapq
import bisect
from collections import defaultdict
import math

# -----------------------
# Базовые структуры
# -----------------------

class Edge:
    def __init__(self, to, weight):
        self.to = to
        self.weight = weight

class Node:
    def __init__(self, node_id, x=0.0, y=0.0):
        self.id = node_id
        self.x = x
        self.y = y
        self.edges = []          # pedestrian edges (undirected in graph)
        self.stop_routes = []    # list of route_ids that serve this node (if any)
        self.clusters = set()    # cluster ids this node belongs to

class Route:
    def __init__(self, route_id, stops, travel_times, arrivals):
        """
        stops: list of node_ids in order
        travel_times: list len = len(stops)-1, travel_times[i] is time from stops[i] -> stops[i+1]
        arrivals: list of lists; arrivals[pos][trip_idx] = absolute arrival time of trip_idx at stops[pos]
                  for a given route all arrivals[pos] must have same length (#trips)
        """
        self.id = route_id
        self.stops = stops
        self.travel_times = travel_times
        self.arrivals = arrivals  # 2D list

# -----------------------
# Graph container
# -----------------------

class Graph:
    def __init__(self):
        self.nodes = {}  # node_id -> Node
        self.routes = {} # route_id -> Route
        # helper: for route quick pos lookup
        self.stop_to_route_pos = {}  # route_id -> {node_id: pos_index}

    def add_node(self, node_id, x=0.0, y=0.0):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, x, y)
        return self.nodes[node_id]

    def add_undirected_edge(self, u, v, weight):
        # undirected pedestrian edge
        self.add_node(u)
        self.add_node(v)
        self.nodes[u].edges.append(Edge(v, weight))
        self.nodes[v].edges.append(Edge(u, weight))

    def add_route(self, route: Route):
        self.routes[route.id] = route
        self.stop_to_route_pos[route.id] = {}
        for i, stop in enumerate(route.stops):
            self.add_node(stop)
            self.nodes[stop].stop_routes.append(route.id)
            self.stop_to_route_pos[route.id][stop] = i

# -----------------------
# Dijkstra ограниченный (до k найденных вершин)
# -----------------------

def dijkstra_limited(graph: Graph, source_id, k, stop_ids_to_halt=set(), banned_internals=set()):
    dist = {source_id: 0.0}
    heap = [(0.0, source_id)]
    visited = set()
    members = set()

    while heap and len(members) < k:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue

        # 1) Если это другая остановка того же маршрута — не включаем, не расширяем
        if u in stop_ids_to_halt and u != source_id:
            visited.add(u)
            continue

        # 2) Если это внутренняя точка другого кластера — включаем, но не расширяем
        if u in banned_internals and u != source_id:
            visited.add(u)
            members.add(u)
            continue

        # 3) Нормальная вершина — включаем и расширяем
        visited.add(u)
        members.add(u)

        for e in graph.nodes[u].edges:
            v = e.to
            nd = d + e.weight
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    filtered_dist = {v: dist[v] for v in members}
    return members, filtered_dist


# -----------------------
# Построение кластеров
# -----------------------

def build_clusters(graph: Graph, route_stops_map, k):
    """
    route_stops_map: route_id -> list of node_ids (остановки в порядке маршрута)
    Возвращает clusters dict:
      cluster_id -> {'members': set, 'boundary': set, 'internal': set}
    """
    clusters = {}
    membered_internals = set()
    cid_seq = 0

    # Перебираем все маршруты и их остановки, создаём кластер вокруг каждой остановки
    for route_id, stops in route_stops_map.items():
        stop_set = set(stops)
        for stop_node in stops:
            cid = f"cl{cid_seq}"
            cid_seq += 1
            if len(graph.nodes[stop_node].clusters) != 0:
                continue
            members, dmap = dijkstra_limited(graph, stop_node, k,
                                             stop_ids_to_halt=stop_set,
                                             banned_internals=membered_internals)

            clusters[cid] = {'members': set(members), 'boundary': set()}
            # пометить занятные точки
            for v in clusters[cid]['members']:
                membered_internals.add(v)


            for v in members:
                graph.nodes[v].clusters.add(cid)
                # отнесём вершины к boundary если вершина уже была в кластерах
                if len(graph.nodes[v].clusters) > 1:
                    # пометим как boundary во всех кластерах
                    for clusterId in graph.nodes[v].clusters:
                        clusters[clusterId]['boundary'].add(v)

    return clusters

# -----------------------
# Прекомпьют всех пар внутри кластера (Dijkstra из каждой вершины)
# -----------------------

def dijkstra_extract_distances(graph: Graph, source_id, target_set):
    dist = {source_id: 0.0}
    heap = [(0.0, source_id)]
    visited = set()
    res = {}
    remaining = set(target_set)
    while heap and remaining:
        d,u = heapq.heappop(heap)
        if u in visited: continue
        visited.add(u)
        if u in remaining:
            res[u] = d
            remaining.remove(u)
        for e in graph.nodes[u].edges:
            v = e.to
            nd = d + e.weight
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return res

def precompute_intra_cluster_distances(graph: Graph, clusters):
    """
    Возвращает cluster_dist:
      cluster_dist[cid][u][v] = distance u->v внутри кластера cid (если достижимо)
    """
    cluster_dist = {}
    for cid, info in clusters.items():
        members = info['members']
        cluster_dist[cid] = {}
        for u in members:
            cluster_dist[cid][u] = dijkstra_extract_distances(graph, u, members)
    return cluster_dist

# -----------------------
# Сжатый граф (boundary vertices + все остановки)
# -----------------------

class CompressedGraph:
    def __init__(self):
        self.adj = defaultdict(list)  # u -> list of (v, weight)
        self.nodes = set()

def build_compressed_graph(graph: Graph, clusters, cluster_dist):
    comp = CompressedGraph()
    for cid, info in clusters.items():
        members = info['members']
        interesting = set(info['boundary'])
        # добавить остановки в interesting
        for v in members:
            if graph.nodes[v].stop_routes:
                interesting.add(v)
        # заполнить узлы
        for u in interesting:
            comp.nodes.add(u)
        # рёбра внутри кластера между интересующими вершинами
        for u in interesting:
            dmap = cluster_dist[cid].get(u, {})
            for v in interesting:
                if u == v:
                    continue
                if v in dmap:
                    comp.adj[u].append((v, dmap[v]))
    return comp

# -----------------------
# Модифицированный Dijkstra с учётом поездок по расписанию
# -----------------------

def next_trip_index(arrivals_list, current_time):
    """Возвращает индекс trip >= current_time, либо None"""
    i = bisect.bisect_left(arrivals_list, current_time)
    if i < len(arrivals_list):
        return i
    return None

def modified_dijkstra_with_transit(graph: Graph, comp_graph: CompressedGraph,
                                   clusters, cluster_dist,
                                   start_id, target_id, start_time):
    """
    Возвращает tuple (best_arrival_time, prev_map)
    prev_map: node_id -> (prev_node, action)
      action: ('walk',)  # пришли пешком
              ('wait', route_id, trip_idx)  # ждали на той же остановке и затем (возможно) сели
              ('ride', route_id, trip_idx)  # пришли на node из поездки route_id trip_idx
    """
    INF = float('inf')
    dist = defaultdict(lambda: INF)
    prev = {}  # node -> (prev_node, action)
    pq = []

    # initialize: положим в очередь стартовую вершину
    dist[start_id] = start_time
    heapq.heappush(pq, (start_time, start_id))

    # также добавляем сразу интересующие вершины из кластеров стартовой вершины
    start_clusters = graph.nodes[start_id].clusters
    if start_clusters:
        for cid in start_clusters:
            members = clusters[cid]['members']
            interesting = set(clusters[cid]['boundary'])
            for v in members:
                if graph.nodes[v].stop_routes:
                    interesting.add(v)
            dmap = cluster_dist[cid].get(start_id, {})
            for v in interesting:
                if v == start_id:
                    continue
                if v in dmap:
                    t_arr = start_time + dmap[v]
                    if t_arr < dist[v]:
                        dist[v] = t_arr
                        prev[v] = (start_id, ('walk',))
                        heapq.heappush(pq, (t_arr, v))

    target_clusters = graph.nodes[target_id].clusters

    while pq:
        cur_time, u = heapq.heappop(pq)
        if cur_time != dist[u]:
            continue

        # если u и target имеют общий кластер — можем завершить быстро, если известна внутренняя дистанция
        if graph.nodes[u].clusters & target_clusters:
            intersect = graph.nodes[u].clusters & target_clusters
            best_total = INF
            for cid in intersect:
                dmap = cluster_dist[cid].get(u, {})
                if target_id in dmap:
                    cand = cur_time + dmap[target_id]
                    if cand < best_total:
                        best_total = cand
            if best_total < INF:
                # установим prev для target (чтобы восстановить) и вернём
                prev[target_id] = (u, ('walk_to_target_in_cluster',))
                dist[target_id] = best_total
                return best_total, prev

        # 1) раскрываем компрессированные пешеходные рёбра (walk между boundary/stop)
        for v, w in comp_graph.adj.get(u, []):
            arrival = cur_time + w
            if arrival < dist[v]:
                dist[v] = arrival
                prev[v] = (u, ('walk',))
                heapq.heappush(pq, (arrival, v))

        # 2) если u — остановка, обработать маршруты (wait/ride)
        node_obj = graph.nodes[u]
        if node_obj.stop_routes:
            for route_id in node_obj.stop_routes:
                route = graph.routes[route_id]
                pos = graph.stop_to_route_pos[route_id][u]
                arrivals_here = route.arrivals[pos]  # list of times for trips at this stop

                trip_idx = next_trip_index(arrivals_here, cur_time)
                if trip_idx is None:
                    continue

                arrival_time_here = arrivals_here[trip_idx]
                if arrival_time_here > cur_time:
                    # надо ждать: добавляем саму точку u с временем arrival_time_here
                    # action 'wait' означает, что позже при обработке мы сядем на trip_idx
                    if arrival_time_here < dist[u]:
                        dist[u] = arrival_time_here
                        prev[u] = (u, ('wait', route_id, trip_idx))
                        heapq.heappush(pq, (arrival_time_here, u))
                    # после ожидания мы обработаем посадку (попади снова на эту вершину)
                else:
                    # можем сразу сесть на trip_idx
                    # переберём все последующие остановки и положим их с их times
                    # предположение: route.arrivals[p][trip_idx] даёт время прибытия этого же trip на stop p
                    for p in range(pos + 1, len(route.stops)):
                        dest_node = route.stops[p]
                        arrival_at_dest = route.arrivals[p][trip_idx]
                        # добавить в очередь
                        if arrival_at_dest < dist[dest_node]:
                            dist[dest_node] = arrival_at_dest
                            prev[dest_node] = (u, ('ride', route_id, trip_idx))
                            heapq.heappush(pq, (arrival_at_dest, dest_node))

        # 3) раскрывать "локальные" несжатые соседи внутри кластеров не обязательно,
        #    но можно при желании — здесь пропускаем (оптимизация). Если нужно, добавить.

    return None, prev  # путь не найден

# -----------------------
# Восстановление пути (простая версия)
# -----------------------

def reconstruct_path(prev_map, start_id, target_id):
    """
    prev_map: node -> (prev_node, action)
    Возвращаем список событий в порядке (start -> ... -> target):
      [(node_id, action_desc, time_unknown), ...]
    Заметьте: точные времена не реконструируются здесь (они в dist). Мы возвращаем только последовательность узлов и тип перехода.
    """
    if target_id not in prev_map:
        return None
    path_nodes = []
    cur = target_id
    while True:
        entry = prev_map.get(cur)
        if entry is None:
            # возможно cur == start и не имел prev
            path_nodes.append((cur, 'start'))
            break
        prev_node, action = entry
        path_nodes.append((cur, action))
        if prev_node == cur:
            # например, wait event stored as (u, ('wait',...)) - перерыв, но всё равно надо остановиться если prev_node == cur and no further
            # чтобы избежать бесконечного цикла, проверяем если у этого узла дальше нет prev или prev == cur -> stop
            # попытаемся взять prev of prev_node:
            nxt = prev_map.get(prev_node)
            if not nxt or nxt[0] == prev_node:
                # reached beginning
                path_nodes.append((prev_node, 'start'))
                break
            else:
                cur = prev_node
                continue
        if prev_node == None:
            break
        cur = prev_node
        if cur == start_id:
            path_nodes.append((cur, 'start'))
            break
    path_nodes.reverse()
    return path_nodes

# -----------------------
# Пример использования (микро-тест)
# -----------------------

def example():
    g = Graph()

    # создадим простую пешеходную сетку:
    # nodes: 1--2--3
    #        |  |
    #        4--5
    g.add_node(1); g.add_node(2); g.add_node(3); g.add_node(4); g.add_node(5)
    g.add_undirected_edge(1,2, 1.0)
    g.add_undirected_edge(2,3, 1.0)
    g.add_undirected_edge(1,4, 1.5)
    g.add_undirected_edge(4,5, 1.0)
    g.add_undirected_edge(5,2, 1.2)

    # добавим маршрут (транспорт) routeA: 1 -> 2 -> 3
    # trips: two trips: trip0 at times [5,6,7] (arrival at stops 1,2,3),
    #                   trip1 at times [15,16,17]
    routeA = Route(
        'A',
        stops=[1,2,3],
        travel_times=[1.0, 1.0],
        arrivals=[
            [5.0, 15.0],   # stop 1 arrivals for trip0 and trip1
            [6.0, 16.0],   # stop 2
            [7.0, 17.0]    # stop 3
        ]
    )
    g.add_route(routeA)

    # второй маршрут B: 4 -> 5 -> 2
    routeB = Route(
        'B',
        stops=[4,5,2],
        travel_times=[1.0, 1.2],
        arrivals=[
            [3.0, 13.0],   # stop4
            [4.0, 14.0],   # stop5
            [5.2, 15.2]    # stop2
        ]
    )
    g.add_route(routeB)

    # подготовка: route_stops_map
    route_stops_map = {rid: r.stops for rid,r in g.routes.items()}

    # кластеризация (берём k=4)
    k = 4
    clusters = build_clusters(g, route_stops_map, k)
    print("Clusters built:", clusters.keys())
    for cid, info in clusters.items():
        print(cid, "members:", info['members'], "boundary:", info['boundary'], "internal:", info['internal'])

    # прекомпьют
    cluster_dist = precompute_intra_cluster_distances(g, clusters)

    # сжатый граф
    comp = build_compressed_graph(g, clusters, cluster_dist)
    print("Compressed nodes:", comp.nodes)
    for u, lst in comp.adj.items():
        print("comp edge", u, "->", lst)

    # запустим поиск: от node 4 к node 3, старт в time = 2.0
    start_id = 4
    target_id = 3
    start_time = 2.0

    best_time, prev = modified_dijkstra_with_transit(g, comp, clusters, cluster_dist, start_id, target_id, start_time)
    print("Best arrival time:", best_time)
    path = reconstruct_path(prev, start_id, target_id)
    print("Path (nodes and actions):")
    for p in path:
        print(p)

if __name__ == "__main__":
    example()
