from datetime import datetime

from my_code.code.algos.transport_routes import TransportRoute, TransportRoutes
from my_code.code.transport.get_stops import get_nearest_points


def get_model_route(file, name,  d_stop: dict[str, int], d_routes : dict[tuple[str, datetime], tuple[str, datetime]]) -> TransportRoute:
    d_id = get_nearest_points(file, d_stop)

    result_routes = []
    i = 0
    for route_name, route_instances in d_routes.items():
        i += 1
        transport_route = get_model_route(i, route_name, d_id, route_instances)
        result_routes.append(transport_route)
    return TransportRoutes(result_routes)