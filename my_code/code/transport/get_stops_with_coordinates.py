import os
import time
import json
from my_code.code.transport.classes import Stop, Point, RouteCoordinates
from my_code.code.utilite import get_slow_query, get_slow_query_bad, get_coordinates
import re


def get_stops_with_coordinates(ref) -> tuple[list[Stop], list[Point]]:
    s = get_slow_query(ref + '/map', 15)
    scripts_without_attrs = [str(script) for script in s.find_all('script') if len(script.attrs) == 1]
    filtered_script = filter(lambda c: 'drawMap(' in c, scripts_without_attrs)
    script = list(filtered_script)[0]
    pattern_stop = r"({\"name\":\".+?})"
    pattern_coordinates = r"(\[\[[\[\d, .\]]+?]])"

    stops = re.findall(pattern_stop, str(script))
    coordinates_path = re.findall(pattern_coordinates, str(script))
    stops_object = []
    for stop in stops:
        stop_dict = json.loads(stop)
        stops_object.append(Stop(stop_dict['name'], float(stop_dict['lat']), float(stop_dict['long'])))

    coordinates_object = []
    coordinates_path[0] = coordinates_path[0][1:]
    start_lan, start_lon = stops_object[0].lat, stops_object[0].lon
    coordinates_object.append(Point(start_lan, start_lon))

    for i in range(len(coordinates_path)):
        points = coordinates_path[i][2:-3].split('],[')
        for point_str in points:
            point_s = point_str.split(',')
            lan, lon = float(point_s[0]), float(point_s[1])
            coordinates_object.append(Point(lan, lon))
        point_stop = stops_object[i + 1]
        coordinates_object.append(Point(point_stop.lat, point_stop.lon))
    return stops_object, coordinates_object

def get_cashed_stops_with_coordinates(name_city, name, ref) -> RouteCoordinates:
    path = f"../transport/data_coordinates/{name_city}.txt"
    if not os.path.exists(path):
        with open(path, 'w') as file:
            file.write('')
    if get_coordinates(name_city, name) is None:
        stops_object, coordinates_object = get_stops_with_coordinates(ref)
        obj_for_json = RouteCoordinates(name, stops_object, coordinates_object)
        with open(path, 'a', encoding='utf-8') as file:
            file.write(f'{name}\t{obj_for_json.to_json()}\n')
        return obj_for_json
    else:
        return get_coordinates(name_city, name)







