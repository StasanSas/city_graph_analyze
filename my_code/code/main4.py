import time

from my_code.code.algos.clusterization.cash_data_clusterization import write_data, get_path_cluster_file, get_data, \
    get_cashed_cluster_data
from my_code.code.algos.clusterization.get_clusters import get_clusters
from my_code.code.exper.calculate_statistic_clusterization import calculate_statistic_by_clusters, draw_plt
from my_code.code.exper.draw_plot_by_x_and_y import draw_plot_by_x_and_y
from my_code.code.exper.visualize import find_and_visualize_clusters_in_ares
from my_code.code.utilite import read_graphml

if __name__ == '__main__':
    path = "one_component__and__without_2_chains/Moscow.graphml"
    x = []
    y = []
    for size_d in range(5, 86, 5):
        s = time.time()
        res_clusterization = get_cashed_cluster_data(path, float(size_d))
        t = time.time() - s
        print(f'{t // 60} минут {t % 60} секунд')

        x.append(size_d)
        y.append(len(res_clusterization))
    draw_plot_by_x_and_y(x, y)
    #edges, sizes = calculate_statistic_by_clusters(res_clusterization)
    #graph = read_graphml(path)

    #find_and_visualize_clusters_in_ares(
    #   graph, res_clusterization,
    #   center_lat=55.7522,
    #   center_lon=37.6156,
    #   size_cluster=30,
    #   name_city="Moscow",
    #   radius_km=2
    #
    #draw_plt(edges, "Группа", "Длинна", "Длины рёбер")
    #draw_plt(sizes, "Группа", "Размер", "Размер групп")
