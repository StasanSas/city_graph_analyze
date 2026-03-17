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
with open('../transport/data_coordinates/Kostroma/Автобус 3.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    answer_stop = RouteCoordinates.from_json(content)
    area_center = [57.76294207100577, 40.942512392779435]
    school_map = folium.Map(location=area_center, zoom_start=12)
    file_name = 'try11.html'
    locations = []
    for point in answer_stop.points:
        locations.append((point.x, point.y))
    folium.PolyLine(locations=locations, color='blue', weight=5).add_to(school_map)
    school_map.save(file_name)
