from math import degrees

from my_code.code.algos.clusterization.ResultClusterization import ResultClusterization
from my_code.code.algos.clusterization.dijstra_from_many_sourses import get_big_tree, getter_neighbors
from my_code.code.algos.clusterization.get_best_center import get_best_cluster
from my_code.code.algos.dijkstra_transport import DijkstraWithTransport
from my_code.code.algos.h3_helper.h3_index import get_h3_resolution_for_current_size, H3Index
from my_code.code.getter_city_data.getter_nk_graph import nx_to_nk_with_extra
from my_code.code.utilite import read_graphml
import networkit as nk
import networkit.distance


def get_clusters(part_path_input : str, size_d : float, have_clusters = False) -> ResultClusterization:
        graph = read_graphml(part_path_input)
        graph_nk, coordinates_data = nx_to_nk_with_extra(graph)
        h3_resolution = get_h3_resolution_for_current_size(8 * size_d)
        result = ResultClusterization()

        if have_clusters:
            result.have_clusters = True
        print(graph_nk.numberOfNodes())
        while graph_nk.numberOfNodes() > 0:
            h3_index = H3Index(coordinates_data, h3_resolution)
            h3_centers = h3_index.get_stupid_center(graph_nk)
            gener_n = getter_neighbors(graph_nk)
            trees = get_big_tree(gener_n, h3_centers, 5 * size_d, 10)
            node_for_delete = []
            for center, tree in trees.items():
                cluster = get_best_cluster(gener_n, tree, size_d)
                node_for_delete.extend(cluster.nodes)
                result.centers.add(cluster.center)
                if have_clusters:
                    result.clusters.append(cluster)
            for node in node_for_delete:
                if graph_nk.hasNode(node):
                    graph_nk.removeNode(node)
                    del coordinates_data[node]
            print(graph_nk.numberOfNodes())
        return result





