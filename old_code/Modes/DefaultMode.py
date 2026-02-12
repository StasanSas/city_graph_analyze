import osmium
from old_code.DrawerInfo import DrawerInfo
from old_code.Graphs.Graph import Graph


class DefaultMode:

    def __init__(self, file):
        self.tags = []
        self.area_file = file
        self.drawer_info = DrawerInfo()  # супер временная переменная для отрисовки
        # мб понадобится переменная с названием режима
        self.graph = Graph()


    # надо оптимизировать, мб сразу все теги смотреть
    def get_graph(self):
        target_dict = {}
        for key, value in self.tags:
            target_dict.setdefault(key, set()).add(value)

        for obj in osmium.FileProcessor(self.area_file).with_locations():
            for tag in obj.tags:
                if (tag.k in target_dict and
                        tag.v in target_dict[tag.k]):
                    self.add_object(obj)
                    break  # объект подходит, переходим к следующему
        return self.graph

    def add_object(self, obj):
        if obj.is_way():
            nodes = obj.nodes
            if len(nodes) > 0:
                self.graph.add_way(nodes)
                self.drawer_info.add_way(nodes)  # супер временная строчка для отрисовки

    def get_shortest_route(self, start, end):
        shortest_route = self.graph.get_shortest_route(start, end)
        return shortest_route