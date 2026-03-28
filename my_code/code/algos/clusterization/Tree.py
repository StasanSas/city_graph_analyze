
class Tree:
    nodes: set[int]
    edges: set[tuple[int, int]]
    sum_distance: float

    def __init__(self):
        self.nodes: set[int] = set()
        self.edges: set[tuple[int, int, float]] = set()
        self.sum_distance: float = 0

    def get_score(self):
        return (len(self.nodes), self.sum_distance / (len(self.nodes) + 0.5))