import time
from typing import List

import requests
from bs4 import BeautifulSoup

from my_code.code.algos.h3_helper.h3_index import H3Index
from my_code.code.getter_city_data.getter_nk_graph import nx_to_nk_with_extra
from my_code.code.transport.classes import Stop, Point
from my_code.code.utilite import get_slow_query, read_graphml, haversine

index = None

def get_d_with_one_point(stops: List[Stop]) -> dict[str, Point]:
    d_list = {}

    for stop in stops:
        if stop.name not in d_list:
            d_list[stop.name] = [Point(stop.lon, stop.lat)]
        else:
            d_list[stop.name].append(Point(stop.lon, stop.lat))

    d_result = {}
    for stop in d_list.keys():
        point_lat, point_lon = 0, 0
        for point in d_list[stop]:
            point_lon += point.lon
            point_lat += point.lat
        l = len(d_list[stop])
        d_result[stop] = Point(point_lon / l, point_lat / l)
    return d_result

def get_id_dict_for_file(d : dict[str, Point], index : H3Index) -> dict[str, int]:
    result = {}
    for name, point in d.items():
        found_nearest = index.nearest(point.lat, point.lon)
        if found_nearest is not None:
            result[name.title()] = found_nearest
    return result

def get_dict_id_in_graph_by_name_stop(stops: List[Stop], index : H3Index) -> dict[str, int]:
    d_point_by_name_stop = get_d_with_one_point(stops)
    result = get_id_dict_for_file(d_point_by_name_stop, index)
    return result



