from my_code.code.transport.get_all_urls import city_with_graph_and_transport_urls
from my_code.code.transport.get_stops import get_dict_stops

data_source_city = city_with_graph_and_transport_urls()

data_stops_kostroma = get_dict_stops('../city_graphs/' + 'Kostroma_graph.osm.pbf')
c = 0
bad_coordinates = []
for id, v in data_stops_kostroma.items():
    x, y, data = v
    name = data['name'] if 'name' in data else 'pizdes'
    if (name == 'pizdes'):
        bad_coordinates.append((x, y))
    print(f'{name} \n({x} , {y})\n')
print(c)


#for name, source in data_source_city.items():
    #file, url = source
    #stops_data = get_dict_stops('../city_graphs/' + file)
    #a = 0
