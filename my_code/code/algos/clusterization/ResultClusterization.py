from my_code.code.algos.clusterization.Cluster import Cluster


class ResultClusterization:
    center : set[int]
    clusters : list[Cluster]
    have_clusters: bool

    def __init__(self):
        self.centers = []
        self.clusters = []
        self.have_clusters = False