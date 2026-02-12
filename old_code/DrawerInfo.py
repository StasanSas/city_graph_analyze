class DrawerInfo:
    def __init__(self):
        self.nodes_locations = set()  # для рисования узлов
        self.ways = []  # больше для рисования

    def add_node(self, obj):
        self.nodes_locations.add((obj.lat, obj.lon))

    def add_way(self, nodes):
        k = []
        for i in range(len(nodes)):
            curr_node = nodes[i]
            self.nodes_locations.add((curr_node.lat, curr_node.lon, curr_node.ref))  # рисование
            k.append((curr_node.lat, curr_node.lon))  # рисование2
        self.ways.append(k)  # для рисования

    def get_nodes(self):
        return self.nodes_locations

    def get_ways(self):
        return self.ways