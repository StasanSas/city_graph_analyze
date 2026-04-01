import heapq
from typing import Any

import h3
import networkx as nx
import networkit as nk

from my_code.code.utilite import haversine

def get_h3_resolution_for_current_size(size_in_metter : float) -> int:
    for resolution in range(15, -1, -1):
        h3_radius = h3.average_hexagon_edge_length(resolution, unit='m')
        if h3_radius > size_in_metter:
            return resolution



class H3Index:
    def __init__(self, coords: dict[int, dict[str, float]], resolution: int = 10):
        """
        coords: {node_id: (lat, lon)}
        resolution: H3 resolution
        """
        self.resolution = resolution
        self.coords = {id : (d['y_coord'], d['x_coord']) for id, d in coords.items()}
        self.cells = {}

        for node_id, d in coords.items():
            cell = h3.latlng_to_cell(d['y_coord'], d['x_coord'], resolution)
            self.cells.setdefault(cell, []).append(node_id)

    def nearest(self, lat: float, lon: float, k: int = 1, max_distance = 300) -> int | None:
        """
        Возвращает id ближайшей вершины из словаря за O(1) по координатам
        """
        query_point = (lat, lon)
        cell = h3.latlng_to_cell(lat, lon, self.resolution)

        candidates = set()
        ring = 0

        while len(candidates) < k:
            cells = h3.grid_disk(cell, ring)

            for c in cells:
                if c in self.cells:
                    candidates.update(self.cells[c])

            ring += 1
            if ring > 8:
                break

        distances = [
            (node_id, haversine(query_point, self.coords[node_id]))
            for node_id in candidates
        ]

        nearest_nodes = heapq.nsmallest(k, distances, key=lambda x: x[1])

        if len(nearest_nodes) == 0:
            return None

        best_node, best_dist = nearest_nodes[0]

        if best_dist > max_distance:
            return None

        return best_node



    def get_stupid_center(self, graph: nk.Graph):
        result = []

        for cell, node_ids in self.cells.items():
            nodes_sortes = sorted(node_ids, key=lambda node_id: graph.degree(node_id), reverse=True)
            lat, lng = h3.cell_to_latlng(cell)
            nodes_sortes = sorted(nodes_sortes, key=lambda node_id: haversine((lat, lng), self.coords[node_id]))
            result.append(nodes_sortes[0])
        return result


