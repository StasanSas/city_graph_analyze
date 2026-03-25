
class Tree:
    nodes: set[int]
    edges: set[tuple[int, int]]
    sum_distance: float

    def get_score(self):
        return (len(self.nodes), self.sum_distance / (len(self.nodes) + 0.5))