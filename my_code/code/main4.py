from my_code.code.algos.clusterization.get_clusters import get_clusters
from my_code.code.exper.calculate_statistic_clusterization import calculate_statistic_by_clusters, draw_plt
from my_code.code.exper.visualize import find_and_visualize_clusters_in_ares
from my_code.code.utilite import read_graphml

if __name__ == '__main__':
    path = "one_component__and__without_2_chains/Kostroma.graphml"
    res_clusterization = get_clusters(path, 30.0, have_clusters=True)
    edges, sizes = calculate_statistic_by_clusters(res_clusterization.clusters)
    graph = read_graphml(path)

    find_and_visualize_clusters_in_ares(
        graph, res_clusterization.clusters,
        center_lat=57.76294207100577,
        center_lon=40.942512392779435,
        size_cluster=30,
        radius_km=6
    )
    #draw_plt(edges, "Группа", "Длинна", "Длины рёбер")
    #draw_plt(sizes, "Группа", "Размер", "Размер групп")
