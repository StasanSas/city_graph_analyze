from math import degrees

from my_code.code.algos.dijkstra_transport import DijkstraWithTransport
from my_code.code.algos.h3_helper.h3_index import get_h3_resolution_for_current_size, H3Index
from my_code.code.getter_city_data.getter_nk_graph import nx_to_nk_with_extra
from my_code.code.utilite import read_graphml
import networkit as nk
import networkit.distance


def get_clusters(part_path_input : str, size_d : float) -> None:
        graph = read_graphml(part_path_input)
        graph_nk, coordinates_data = nx_to_nk_with_extra(graph)
        h3_resolution = get_h3_resolution_for_current_size(size_d)
        node_for_delete = set()
        result = set()

        while len(graph_nk.numberOfNodes() > 0):
            h3_index = H3Index(coordinates_data, h3_resolution)
            h3_centers = h3_index.get_stupid_center(graph_nk)


