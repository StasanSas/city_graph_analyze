from typing import List, Dict, Tuple

import networkx as nx
import numpy as np


def compress_linear_paths(graph: nx.Graph,
                          max_compression_length: float = 5000,  # метров
                          preserve_nodes: set = None) -> nx.Graph:
    """
    Склеивает линейные пути без ветвлений в одно ребро
    """
    if preserve_nodes is None:
        preserve_nodes = set()

    compressed_graph = graph.copy()
    processed_nodes = set()
    compression_count = 0

    for node in list(compressed_graph.nodes()):
        if node in processed_nodes:
            continue

        # Пропускаем узлы, которые нужно сохранить
        if node in preserve_nodes:
            processed_nodes.add(node)
            continue

        # Ищем линейные цепочки
        linear_chains = _find_linear_chains(compressed_graph, node, preserve_nodes)

        for chain in linear_chains:
            if len(chain) >= 3:  # Минимум 3 узла для склейки
                compressed_graph, count = _compress_chain(compressed_graph, chain,
                                                          max_compression_length)
                compression_count += count
                processed_nodes.update(chain)

    print(f"Склеено {compression_count} линейных цепочек")
    return compressed_graph


def _find_linear_chains(graph: nx.Graph, start_node, preserve_nodes: set) -> List[List]:
    """
    Находит все линейные цепочки, начинающиеся с узла
    """
    chains = []
    visited = set()

    def dfs_linear_path(current_node, current_path):
        if current_node in visited or current_node in preserve_nodes:
            return

        visited.add(current_node)
        current_path.append(current_node)

        neighbors = list(graph.neighbors(current_node))

        # Фильтруем соседей, которые уже в пути или должны сохраняться
        valid_neighbors = [n for n in neighbors
                           if n not in current_path and n not in preserve_nodes]

        # Линейный узел имеет ровно 2 связи (вход и выход)
        if len(valid_neighbors) == 1:
            dfs_linear_path(valid_neighbors[0], current_path)
        else:
            # Конец цепочки
            if len(current_path) >= 3:
                chains.append(current_path.copy())

    dfs_linear_path(start_node, [])
    return chains


def _compress_chain(graph: nx.Graph, chain: List, max_length: float) -> Tuple[nx.Graph, int]:
    """
    Склеивает линейную цепочку в одно ребро
    """
    if len(chain) < 3:
        return graph, 0

    start_node = chain[0]
    end_node = chain[-1]

    # Проверяем, что цепочка не слишком длинная
    total_length = 0
    for i in range(len(chain) - 1):
        u, v = chain[i], chain[i + 1]
        if graph.has_edge(u, v):
            total_length += graph[u][v].get('length', 0)

    if total_length > max_length:
        return graph, 0

    # Вычисляем агрегированные атрибуты
    aggregated_data = _aggregate_chain_attributes(graph, chain)

    # Удаляем промежуточные узлы и добавляем новое ребро
    intermediate_nodes = chain[1:-1]

    # Сохраняем оригинальные связи начального и конечного узлов
    start_neighbors = set(graph.neighbors(start_node))
    end_neighbors = set(graph.neighbors(end_node))

    # Удаляем промежуточные узлы
    graph.remove_nodes_from(intermediate_nodes)

    # Добавляем новое сжатое ребро
    if not graph.has_edge(start_node, end_node):
        graph.add_edge(start_node, end_node, **aggregated_data)

    return graph, len(intermediate_nodes)


def _aggregate_chain_attributes(graph: nx.Graph, chain: List) -> Dict:
    """
    Агрегирует атрибуты всей цепочки в один набор данных
    """
    total_length = 0
    max_speeds = []
    capacities = []
    highway_types = set()
    road_names = set()
    travel_times = 0

    for i in range(len(chain) - 1):
        u, v = chain[i], chain[i + 1]
        if graph.has_edge(u, v):
            data = graph[u][v]

            total_length += data.get('length', 0)
            max_speeds.append(data.get('max_speed', 50))
            capacities.append(data.get('capacity', 0))

            if data.get('highway'):
                highway_types.add(data.get('highway'))
            if data.get('name'):
                road_names.add(data.get('name'))

            travel_times += data.get('travel_time', 0)

    # Создаем агрегированные данные
    aggregated = {
        'length': total_length,
        'max_speed': np.mean(max_speeds) if max_speeds else 50,
        'capacity': np.mean(capacities) if capacities else 0,
        'travel_time': travel_times,
        'original_segments': len(chain) - 1,
        'compressed': True,
        'node_chain': chain  # Сохраняем оригинальную цепочку для детализации
    }

    if highway_types:
        aggregated['highway'] = list(highway_types)[0]  # Берем первый тип
        if len(highway_types) > 1:
            aggregated['highway_types'] = list(highway_types)

    if road_names:
        aggregated['name'] = '; '.join(road_names)

    return aggregated