from datetime import datetime

import osmium
import networkx as nx


from my_code.code.transport.classes import Route, Stop, Point, RouteCoordinates
from my_code.code.transport.get_all_names_route_and_ref import get_all_names_route_and_ref, set_process_source
from my_code.code.transport.get_stops_with_coordinates import get_cashed_stops_with_coordinates
from my_code.code.utilite import get_slow_query



def d_with_new_stops(d, route_objects: RouteCoordinates):
    for r in route_objects.stops:
        name = r.name
        if name in d:
            continue
        d[name] = r
    return d

def get_route_objects(url) -> list:
    pass

def get_route_from_object(d, route_objects) -> Route:
    pass

def get_normalized_route(route) -> dict[tuple[str, datetime], tuple[str, datetime]]:
    pass

def get_nearest_points(file, stops) -> dict[str, int]:
    pass



def get_all_routes_with_coordinates_and_time(base_url, name_city):
    d_stop = {} # name_stop : Stop
    d_routes = {} # name_routes : Route
    names_and_ref = get_all_names_route_and_ref(base_url, name_city)
    for name, url in names_and_ref.items():
        try:
            coordinates_data = get_cashed_stops_with_coordinates(name_city, name, url)
            d_stop = d_with_new_stops(d_stop, coordinates_data)

            #route_objects = get_route_objects(url)
            #for route_object in route_objects:
                #route = get_route_from_object(d_stop, route_object)
                #d_routes[route.name] = get_normalized_route(route)
            set_process_source(name_city, url)
        except Exception as e:
            print(e)
    return d_stop, d_routes










