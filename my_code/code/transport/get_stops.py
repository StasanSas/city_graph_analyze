from datetime import datetime
from pathlib import Path
from typing import List

import osmium
import networkx as nx


from my_code.code.transport.classes import Route, Stop, Point, RouteCoordinates, StopTime
from my_code.code.transport.get_normalized_route import get_normalized_route, get_dict_distance
from my_code.code.transport.get_all_names_route_and_ref import get_all_names_route_and_ref, set_process_source
from my_code.code.transport.get_route_time import get_route_times, get_cashed_route_times
from my_code.code.transport.get_stops_with_coordinates import get_cashed_stops_with_coordinates
from my_code.code.transport.getter_coordinates_in_graph import get_dict_id_in_graph_by_name_stop
from my_code.code.utilite import get_slow_query




def get_dict_for_algos(stop_times: List[StopTime], dict_id_by_name : dict[str, int]) -> dict[tuple[str, str], tuple[str, str]]:
    # (id : datatime) : (id : datatime)
    d = {}
    for i in range(0, len(stop_times) - 1):
        stop_time_start = stop_times[i]
        start_times = stop_time_start.time
        start_name = stop_time_start.stop_name
        id_start = dict_id_by_name[start_name]

        stop_time_end = stop_times[i + 1]
        end_times = stop_time_end.time
        end_name = stop_time_end.stop_name
        id_end = dict_id_by_name[end_name]


        for j in range(0, len(stop_time_start.time)):
            start_time = start_times[j]
            end_time = end_times[j]
            d[(id_start, start_time)] = (id_end, end_time)
    return d

def write_dict_subroute(path: str, dict_id_by_name : dict[tuple[str, str], tuple[str, str]]) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        for start, end in dict_id_by_name.items():
            f.write(f'{start[0]}\t{start[1]}\t{end[0]}\t{end[1]}\n')


def load_all_routes_with_coordinates_and_time(base_url, name_city, path_file_city, load_processed = True) -> dict[str, str]:
    d_routes = {} # name_routes : Route
    Path(f"../transport/result/{name_city}").mkdir(parents=True, exist_ok=True)

    names_and_ref = get_all_names_route_and_ref(base_url, name_city, load_processed)
    for name, url in names_and_ref.items():
        try:
            coordinates_data = get_cashed_stops_with_coordinates(name_city, name, url)
            dict_distance = get_dict_distance(coordinates_data)
            dict_id_by_name = get_dict_id_in_graph_by_name_stop(coordinates_data.stops, path_file_city)

            sub_route_times = get_cashed_route_times(name_city, name, url).data_sub_route
            for sub_route_time in sub_route_times:
                corrected_time_route = get_normalized_route(dict_distance, sub_route_time.time_stops)
                d = get_dict_for_algos(corrected_time_route, dict_id_by_name)

                path_name_file = f"../transport/result/{name_city}/{sub_route_time.name}.txt"
                write_dict_subroute(path_name_file, d)

            set_process_source(name_city, url)
        except Exception as e:
            print(e)
    return d_routes










