import os

from my_code.code.algos.clusterization.Cluster import Cluster
from my_code.code.algos.clusterization.get_clusters import get_clusters


def get_path_cluster_file(path : str, size: float):
    parts = path.split('.')
    if len(parts) != 2:
        raise Exception("Не обрабатываем множество расширений или файл без расширения.")
    if parts[1] != "graphml":
        raise Exception("Расширение должно быть .graphml")

    parts_name = parts[0].replace("\\", "/").split('/')
    parts_name.reverse()
    name_file_parts = "_".join(parts_name)


    path_file = f'../clusters_data/{int(size)}_{name_file_parts}.txt'
    os.makedirs(os.path.dirname(path_file), exist_ok=True)
    return path_file
def write_data(clusters : list[Cluster], path : str):
    with open(path, 'w') as f:
        for cluster in clusters:
            f.write(f"{cluster.center}\t{", ".join(map(str, cluster.nodes))}\t{", ".join(map(str, cluster.distances))}\n")

def get_data(path : str) -> list[Cluster]:
    r = []
    with open(path, 'r') as f:
        for line in f.readlines():
            parts = line.split('\t')
            center = int(parts[0])
            nodes = set(map(int, parts[1].split(", ")))
            distances = set(map(float, parts[2].split(", ")))
            c = Cluster()
            c.center = center
            c.nodes = nodes
            c.distances = distances
            r.append(c)
    return r

def get_cashed_cluster_data(path_file_where_clusters : str, size: float) -> list[Cluster]:
    path = get_path_cluster_file(path_file_where_clusters, size)
    if not os.path.exists(path):
        clusters = get_clusters(path_file_where_clusters, size)
        write_data(clusters.clusters, path)
        return clusters.clusters
    return get_data(path)



