import heapq
from typing import Any

import h3

from my_code.code.utilite import haversine


class H3Index:
    def __init__(self, coords: dict[int, dict[str, float]], resolution: int = 10):
        """
        coords: {node_id: (lat, lon)}
        resolution: H3 resolution
        """
        self.resolution = resolution
        self.coords = {id : (d['x_coord'], d['y_coord']) for id, d in coords.items()}
        self.cells = {}

        for node_id, d in coords.items():
            cell = h3.latlng_to_cell(d['x_coord'], d['y_coord'], resolution)
            self.cells.setdefault(cell, []).append(node_id)

    def nearest(self, lat: float, lon: float, k: int = 1) -> Any:
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
            if ring > 10:
                break

        nearest_nodes = heapq.nsmallest(
            k,
            candidates,
            key=lambda node_id: haversine(query_point, self.coords[node_id]),
        )

        return nearest_nodes[0]