import os
import time
import json
from my_code.code.transport.classes import Stop, Point, RouteCoordinates
from my_code.code.utilite import get_slow_query, get_slow_query_bad, get_coordinates
import re


def get_stops_with_coordinates(name, ref) -> RouteCoordinates:
    s = get_slow_query(ref + '/map', 15)
    scripts_without_attrs = [str(script) for script in s.find_all('script') if len(script.attrs) == 1]
    filtered_script = filter(lambda c: 'drawMap(' in c, scripts_without_attrs)
    script = list(filtered_script)[0]
    pattern_stop = r"({\"name\":\".+?})"

    stops = re.findall(pattern_stop, str(script))
    stops_object = []
    for stop in stops:
        stop_dict = json.loads(stop)
        stops_object.append(Stop(stop_dict['name'], float(stop_dict['lat']), float(stop_dict['long'])))
    return RouteCoordinates(name, stops_object)

def get_cashed_stops_with_coordinates(name_city, name, ref) -> RouteCoordinates:
    path = f"../transport/data_coordinates/{name_city}/{name}.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if get_coordinates(name_city, name) is None:
        route_coordinates = get_stops_with_coordinates(name, ref)
        with open(path, 'w', encoding='utf-8') as file:
            file.write(f'{route_coordinates.to_json(ensure_ascii=False, indent=2)}')
        return route_coordinates
    else:
        return get_coordinates(name_city, name)







