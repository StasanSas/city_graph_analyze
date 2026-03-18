from datetime import datetime
from collections import Counter
from typing import List

import numpy as np

from my_code.code.algos.transport_routes import TransportRoute, TransportRoutes
from my_code.code.transport.classes import StopTime, RouteCoordinates, SubRouteTimes, Stop
from my_code.code.transport.get_stops import get_nearest_points
from my_code.code.utilite import get_time_in_min


def get_model_route(file, name,  d_stop: dict[str, int], d_routes : dict[tuple[str, datetime], tuple[str, datetime]]) -> TransportRoute:
    d_id = get_nearest_points(file, d_stop)

    result_routes = []
    i = 0
    for route_name, route_instances in d_routes.items():
        i += 1
        transport_route = get_model_route(i, route_name, d_id, route_instances)
        result_routes.append(transport_route)
    return TransportRoutes(result_routes)


def get_normalized_route(d_stop : dict[str, list[Stop]], stop_times : List[StopTime]) -> dict[tuple[str, datetime], tuple[str, datetime]]:
    # вычисление однозначных координат по названию
    # вычисление "опорных" остановок
    # вычисление максимального расстояния между "опорными точками" и вычисление того, сколько времени тратится на преодоление расстояния
    # получаем скорость движения автобуса
    # вычисление кратчайшего расстояния от не опорной точки до опорной
    # вычисляем время для не опорных точек
    d_stop_new = {}
    for key, value in d_stop.items():
        new_point_y = 0
        new_point_x = 0
        for point in value:
            new_point_x += point.lon
            new_point_y += point.lat
        d_stop_new[key] = (new_point_y / len(value), new_point_x / len(value))

    indexes_where_correct_stops = []
    l_stop_times = list(map(lambda stop_time: len(stop_time.time), stop_times))
    counter = Counter(l_stop_times)
    max_founded_len = counter.most_common(1)[0][0]

    for i in range(len(stop_times)):
        if len(stop_times[i].time) == max_founded_len:
            indexes_where_correct_stops.append(i)

def matrix_stop_times(stop_times : list[StopTime]) -> list[np.ndarray]:
    result = []
    for stop_time in stop_times:
        np_array = np.array(list(map(get_time_in_min, stop_time.time)))
        result.append(np_array)
    return result

def get_speed(d_stop_new : dict[str, tuple[float, float]], indexes_where_correct_stops : list[int], stop_times : list[np.ndarray]) -> None:

    for i in indexes_where_correct_stops:
        is_correct = False
        if i == 0:
            is_correct = True if np.min(stop_times[i+1] - stop_times[i]) >= 0 else False
            is_correct = True if np.min(stop_times[i + 2] - stop_times[i]) >= 0 else False
        if i == len(stop_times) - 1:
            is_correct_1 = True if np.min(stop_times[i] - stop_times[i-1]) >= 0 else False
            is_correct = True if np.min(stop_times[i] - stop_times[i - 2]) >= 0 else False
        else:
            is_correct_1 = True if np.min(stop_times[i + 1] - stop_times[i]) >= 0 else False
            is_correct_2 = True if np.min(stop_times[i] - stop_times[i - 1]) >= 0 else False
            is_correct = is_correct_1 and is_correct_2











    pass