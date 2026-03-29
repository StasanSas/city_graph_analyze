from my_code.code.algos.clusterization.Cluster import Cluster


class ResultClusterization:
    centers : set[int]
    clusters : list[Cluster]
    have_clusters: bool

    def __init__(self):
        self.centers = set()
        self.clusters = []
        self.have_clusters = False