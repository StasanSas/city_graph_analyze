from old_code.Graphs.PublicTransportGraph import PublicTransportGraph
from old_code.Modes.DefaultMode import DefaultMode


class PublicTransportMode(DefaultMode):
    # мб добавить остановки - мб прям в специальное место какое-то



    def __init__(self, file):
        super().__init__(file)
        self.graph = PublicTransportGraph()
        self.tags = [('highway', 'footway'),
                     ('footway', 'crossing'),
                     ('highway', 'pedestrian'),
                     ('highway', 'living_street'),
                     ('footway', 'sidewalk'),
                     ('highway', 'service'),
                     ('highway', 'steps'),
                     ('highway', 'corridor'),
                     ('highway', 'path')]