from datetime import datetime

import osmium
import networkx as nx

from my_code.code.algos.transport_routes import TransportRoute, DataArrival, TransportRoutes
from my_code.code.transport.get_all_names_route_and_ref import get_all_names_route_and_ref
from my_code.code.utilite import get_slow_query
import osmium


class StopRouteHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()

        # id -> (lon, lat, tags)
        self.stops = {}

        # route_id -> route info
        self.routes = {}

    def node(self, n):
        tags = n.tags

        is_stop = (
            tags.get("highway") == "bus_stop"
            or tags.get("railway") == "tram_stop"
            or tags.get("amenity") == "bus_station"
            or tags.get("public_transport") in ["platform", "stop_position"]
        )

        if is_stop:
            self.stops[n.id] = (
                n.location.lon,
                n.location.lat,
                dict(tags),
            )

    def relation(self, r):
        tags = r.tags

        if tags.get("type") != "route":
            return

        route_type = tags.get("route")

        if route_type not in [
            "bus",
            "tram",
            "trolleybus",
            "subway",
            "light_rail",
            "train",
        ]:
            return

        stops = []

        for m in r.members:
            if m.type == "n" and m.role in (
                "stop",
                "platform",
                "stop_entry_only",
                "stop_exit_only",
            ):
                stops.append(m.ref)

        if stops:
            self.routes[r.id] = {
                "type": route_type,
                "name": tags.get("name"),
                "ref": tags.get("ref"),
                "stops": stops,
                "tags": dict(tags),
            }

class Stop:
    def __init__(self, name, lon, lat):
        self.name = name
        self.lon = lon
        self.lat = lat

class Route:
    def __init__(self, name):
        self.name = name
        self.data_stop = [] # [(Stop, [time])]
        self.all_coords = [] # [(lat, lon)]



def get_stops_with_coordinates(base_url, ref) -> list:
    pass

def d_with_new_stops(d, route_objects):
    pass

def get_route_objects(base_url, ref) -> list:
    pass

def get_route_from_object(d, route_objects) -> Route:
    pass

def get_normalized_route(route) -> dict[tuple[str, datetime], tuple[str, datetime]]:
    pass

def get_nearest_points(file, stops) -> dict[str, int]:
    pass

def get_model_route(i, name, d_id : dict[str, int], route : dict[tuple[str, datetime], tuple[str, datetime]]) -> TransportRoute:
    pass

def get_all_routes_with_coordinates_and_time(url, file, name):
    d_stop = {} # name_stop : Stop
    d_routes = {} # name_routes : Route
    names_and_ref = get_all_names_route_and_ref(url, name)
    for name, ref in names_and_ref:
        coordinates_data = get_stops_with_coordinates(url, ref)
        d_stop = d_with_new_stops(d_stop, coordinates_data)

        route_objects = get_route_objects(url, ref)
        for route_object in route_objects:
            route = get_route_from_object(d_stop, route_object)
            d_routes[route.name] = get_normalized_route(route)
    d_id = get_nearest_points(file, d_stop)

    result_routes = []
    i = 0
    for route_name, route_instances in d_routes.items():
        i += 1
        transport_route = get_model_route(i, route_name, d_id, route_instances)
        result_routes.append(transport_route)
    return TransportRoutes(result_routes)










