
class Cluster:
    center : int
    nodes: set[int]
    distances: set[float]

    def __init__(self):
        self.nodes: set[int] = set()
        self.distances: set[float] = set()

    def get_score(self):
        mean_distance = sum(self.distances) / (len(self.distances) + 0.5)
        return (len(self.nodes), - mean_distance)