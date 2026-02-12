from old_code.Drawer import Drawer
from old_code.Modes.ScooterMode import ScooterMode
from old_code.Modes.WalkMode import WalkMode

from old_code.Modes.PublicTransportMode import PublicTransportMode
import time

from old_code.Modes.DefaultMode import DefaultMode


class OSMHandler:
    def __init__(self, start, end, mode, file):
        self.start_coords = start
        self.end_coords = end
        self.mode = mode
        self.file = file

        self.tag_finder = self.get_mode_class()
        self.graph = self.tag_finder.get_graph()
        print(self.graph.get_graph())

    def handle(self):
        self.start_coords, self.end_coords = self.get_node_by_coords(self.start_coords), self.get_node_by_coords(self.end_coords)
        print(self.graph.get_node_coords(self.start_coords), self.graph.get_node_coords(self.end_coords))
        #st, end = 5938255315, 763375415
        start_time = time.time()
        path = self.tag_finder.get_shortest_route(self.start_coords, self.end_coords)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"The task took {elapsed_time:.2f} seconds to complete.")
        drawer = Drawer()
        drawer.draw_route(path)



    def get_mode_class(self):
        if self.mode == 'walk':
            tag_finder = WalkMode(file=self.file)
        elif self.mode == 'scooter':
            tag_finder = ScooterMode(file=self.file)
        elif self.mode == 'PublicTransport':
            tag_finder = PublicTransportMode(file=self.file)
        else:
            tag_finder = DefaultMode(file=self.file)
        return tag_finder


    def get_node_by_coords(self, value):
        sorted_nodes = self.graph.get_sorted_nodes()
        low = 0
        high = len(sorted_nodes) - 1
        best_node = None
        best_distance = float('inf')

        while low <= high:
            mid = (low + high) // 2
            coords = self.graph.get_node_coords(sorted_nodes[mid])

            # Вычисляем расстояние между текущими координатами и искомыми
            distance = self.graph.haversine(coords, value)

            # Если нашли более близкий узел, обновляем best_node
            if distance < best_distance:
                best_distance = distance
                best_node = sorted_nodes[mid]

            # Сравниваем координаты для определения направления поиска
            if coords < value:
                low = mid + 1
            else:
                high = mid - 1

        return best_node

'''
    def get_node_by_coords(self, value):
        sorted_nodes = self.graph.get_sorted_nodes()
        low = 0
        high = len(sorted_nodes) - 1
        mid = len(sorted_nodes) // 2

        coords = self.graph.get_node_coords(sorted_nodes[mid])
        while coords != value and low <= high:
            if value > coords:
                low = mid + 1
            else:
                high = mid - 1
            mid = (low + high) // 2
            coords = self.graph.get_node_coords(sorted_nodes[mid])

        return sorted_nodes[mid]'''


'''
    def get_shortest_path(self, st, end):
        shortest_route_nodes = RouteFinder.get_shortest_route(start_ref=st, end_ref=end,
                                                                  graph=self.graph.get_graph())
        shortest_route_coords = self.graph.get_list_of_nodes_coords(shortest_route_nodes)
        return shortest_route_coords'''