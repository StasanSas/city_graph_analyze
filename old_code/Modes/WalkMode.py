from old_code.Modes.DefaultMode import DefaultMode


class WalkMode(DefaultMode):
    def __init__(self, file):
        super().__init__(file=file)
        self.tags = [('highway', 'footway'), ('footway', 'crossing'), ('highway', 'pedestrian'),
                              ('highway', 'living_street'), ('footway', 'sidewalk'), ('highway', 'service'),
                              ('highway', 'steps'), ('highway', 'corridor'), ('highway', 'path')]
