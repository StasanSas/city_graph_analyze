from my_code.code.transport.get_all_names_route_and_ref import get_all_names_route_and_ref
from my_code.code.transport.get_stops import get_all_routes_with_coordinates_and_time
from my_code.code.utilite import get_slow_query


#|
#s = get_slow_query('https://kudikina.ru/kostr/bus/21k/A', 1)
#scripts_without_attrs = [str(script) for script in s.find_all('script') if len(script.attrs) == 1]
#a = filter(lambda c: 'drawMap(' in c, scripts_without_attrs)
#print(list(a)[0])

#get_all_names_route_and_ref("https://kudikina.ru/kostr/", 'Kostroma')

get_all_routes_with_coordinates_and_time('https://kudikina.ru/mahac', 'Makhachkala')