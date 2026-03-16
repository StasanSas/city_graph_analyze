from datetime import datetime

import osmium
import networkx as nx


from my_code.code.transport.classes import Route, Stop, Point, RouteCoordinates, StopTime
from my_code.code.transport.get_all_names_route_and_ref import get_all_names_route_and_ref, set_process_source
from my_code.code.transport.get_route_time import get_route_times
from my_code.code.transport.get_stops_with_coordinates import get_cashed_stops_with_coordinates
from my_code.code.utilite import get_slow_query



def d_with_new_stops(route_objects: RouteCoordinates) -> dict[str, RouteCoordinates]:
    d = {}
    for r in route_objects.stops:
        name = r.name
        if name in d:
            continue
        d[name] = r
    return d



def get_normalized_route(d_stop : dict[str, RouteCoordinates], route : list[StopTime]) -> dict[tuple[str, datetime], tuple[str, datetime]]:
    pass

def get_nearest_points(file, stops) -> dict[str, int]:
    pass



def get_all_routes_with_coordinates_and_time(base_url, name_city):
    d_routes = {} # name_routes : Route
    names_and_ref = get_all_names_route_and_ref(base_url, name_city)
    for name, url in names_and_ref.items():
        try:
            coordinates_data = get_cashed_stops_with_coordinates(name_city, name, url)
            d_stop = d_with_new_stops(coordinates_data)

            sub_route_times = get_route_times(name, url).data_sub_route
            for sub_route_time in sub_route_times:
                d_routes[sub_route_time.name] = get_normalized_route(d_stop, sub_route_time.time_stops)
            set_process_source(name_city, url)
        except Exception as e:
            print(e)
    return d_routes










