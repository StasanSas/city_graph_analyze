from old_code.Modes.DefaultMode import DefaultMode


class WalkMode(DefaultMode):
    def __init__(self, file):
        super().__init__(file=file)
        self.tags = [
            ('highway','footway'),
            ('highway','pedestrian'),
            ('highway','path'),
            ('highway','steps'),
            ('highway','living_street'),
            ('highway','corridor'),
            ('highway','track'),
            ('highway', 'residential'),
            ('highway', 'secondary'),
            ('highway', 'motorway'),
            ('highway', 'tertiary'),
            ('highway', 'primary'),
            ('highway', 'unclassified'),

            ('footway','sidewalk'),
            ('footway','crossing'),
            ('footway','traffic_island'),

            ('highway','service'),

            ('highway','crossing'),

            ('area:highway','pedestrian')
        ]