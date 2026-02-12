import folium
'''
Пусть он получает только координаты
С графом нет должен взаимодействовать
'''
class Drawer:
    def __init__(self):
        self.area_center = [56.79252, 60.62249]
        self.school_map = folium.Map(location=self.area_center, zoom_start=12)
        self.file_name = 'try11.html'

    #@classmethod
    def draw_route(self, route):
        folium.PolyLine(locations=route, color='red', weight=3).add_to(self.school_map)
        self.school_map.save(self.file_name)

    def draw_nodes(self, nodes):
        for l in nodes:
            lat, lon, id = l
            folium.Marker(location=[lat, lon], popup=str(id)).add_to(self.school_map)
        self.school_map.save(self.file_name)

    def draw_edges(self, ways):
        for k in ways:
            folium.PolyLine(locations=[(lat, lon) for lat, lon in k], color='blue', weight=5).add_to(self.school_map)
        self.school_map.save(self.file_name)