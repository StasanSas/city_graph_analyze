import folium

from my_code.code.transport.classes import RouteCoordinates
from my_code.code.transport.get_all_urls import city_with_graph_and_transport_urls
#from my_code.code.transport.get_stops import get_dict_stops

#data_source_city = city_with_graph_and_transport_urls()

#data_stops_kostroma = get_dict_stops('../city_graphs/' + 'Kostroma_graph.osm.pbf')
#c = 0
#bad_coordinates = []
#for id, v in data_stops_kostroma.items():
#    x, y, data = v
#    name = data['name'] if 'name' in data else 'pizdes'
#    if (name == 'pizdes'):
#        bad_coordinates.append((x, y))
#    print(f'{name} \n({x} , {y})\n')
#print(c)


#for name, source in data_source_city.items():
    #file, url = source
    #stops_data = get_dict_stops('../city_graphs/' + file)
    #a = 0
answer_stop = None
with open('../transport/data_coordinates/Makhachkala/Троллейбус 8.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    answer_stop = RouteCoordinates.from_json(content)
    area_center = [42.964, 47.497]
    school_map = folium.Map(location=area_center, zoom_start=12)
    file_name = 'try11.html'
    for point_list in answer_stop.points:
        locations = []
        for point in point_list:
            locations.append((point.y, point.x))
        folium.PolyLine(locations=locations, color='blue', weight=5).add_to(school_map)
    for stop in answer_stop.stops:
        folium.Marker(location=[stop.lat, stop.lon], popup=stop.name).add_to(school_map)

    school_map.save(file_name)
