from my_code.code.transport.get_all_names_route_and_ref import get_all_names_route_and_ref
from my_code.code.transport.get_stops import load_all_routes_with_coordinates_and_time, write_dict_subroute
from my_code.code.utilite import get_slow_query


#|
#s = get_slow_query('https://kudikina.ru/kostr/bus/1/map', 10)
#scripts_without_attrs = [str(script) for script in s.find_all('script') if len(script.attrs) == 1]
#a = filter(lambda c: 'drawMap(' in c, scripts_without_attrs)
#print(list(a)[0])
a = 0
test = {("a", "b"): ("c", "d"), ("a1", "b1"): ("c1", "d1")}

#write_dict_subroute("test.txt", test)
load_all_routes_with_coordinates_and_time("https://kudikina.ru/kostr/", 'Kostroma', 'one_component__and__without_2_chains/Kostroma.graphml', False)

#load_all_routes_with_coordinates_and_time('https://kudikina.ru/mahac', 'Makhachkala')