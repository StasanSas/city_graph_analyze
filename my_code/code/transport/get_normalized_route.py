from datetime import datetime
from collections import Counter
from typing import List

import numpy as np

from my_code.code.algos.transport_routes import TransportRoute, TransportRoutes
from my_code.code.transport.classes import StopTime, RouteCoordinates, SubRouteTimes, Stop
from my_code.code.utilite import get_time_in_min, haversine, get_str_time



def get_normalized_route(dict_distance: dict[tuple[str, str], float], stop_times : List[StopTime]) -> List[StopTime]:
    # вычисление однозначных координат по названию
    # вычисление "опорных" остановок
    # вычисление максимального расстояния между "опорными точками" и вычисление того, сколько времени тратится на преодоление расстояния
    # получаем скорость движения автобуса
    # вычисление кратчайшего расстояния от не опорной точки до опорной
    # вычисляем время для не опорных точек

    indexes_where_maybe_correct_stops = []
    l_stop_times = list(map(lambda stop_time: len(stop_time.time), stop_times))
    counter = Counter(l_stop_times)
    max_founded_len = counter.most_common(1)[0][0]

    for i in range(len(stop_times)):
        if len(stop_times[i].time) == max_founded_len:
            indexes_where_maybe_correct_stops.append(i)
    matrix = matrix_stop_times_norm(stop_times)
    maybe_correct_indexes = np.array(indexes_where_maybe_correct_stops)

    indexes_correct = get_correct_indexes(maybe_correct_indexes, matrix)

    mask = np.ones(len(stop_times), dtype=bool)
    mask[indexes_correct] = False

    not_correct_indexes = np.where(mask)[0]

    time_list = get_time_move_array(matrix)

    speed = get_speed(indexes_correct, time_list, stop_times, dict_distance)
    stop_times = get_new_times_for_not_correct_stops(indexes_correct, not_correct_indexes, speed, dict_distance, stop_times, matrix)
    return stop_times


def get_speed(indexes_correct : np.ndarray, time_list: list[float], stop_times : List[StopTime], dict_distance: dict[tuple[str, str], float]) -> float:
    start_index, end_index = indexes_correct[0], indexes_correct[-1]
    time_move = time_list[end_index] - time_list[start_index]
    distance = get_final_distance_between_stops(start_index, end_index, stop_times, dict_distance)
    return distance / time_move

def get_new_times_for_not_correct_stops(indexes_correct : np.ndarray, not_correct_indexes : np.ndarray, speed : float,
                                        dict_distance: dict[tuple[str, str], float], stop_times : List[StopTime],
                                        stop_times_matrix : np.ndarray):
    for not_correct_index in not_correct_indexes:
        correct_index, sign_text = get_index_nearest_correct_stop(indexes_correct, not_correct_index)
        distance = get_final_distance_between_stops(correct_index, not_correct_index, stop_times, dict_distance)
        time_delta =  (distance / speed) if sign_text == 'found_smaller' else - (distance / speed)
        new_time = list(stop_times_matrix[not_correct_index, :] + time_delta)
        time_str = list(map(get_str_time, new_time))
        stop_times[not_correct_index].time = time_str
    return stop_times

def get_index_nearest_correct_stop(indexes_correct : np.ndarray, not_correct_index : int) -> tuple[int, str]:
    left_index, right_index = None, None
    for index in indexes_correct:
        if index < not_correct_index:
            left_index = index
        if index > not_correct_index:
            right_index = index
            break
    if left_index is None:
        return (right_index, "found_bigger")
    if right_index is None:
        return (left_index, "found_smaller")
    return (left_index, "found_smaller") if (right_index - not_correct_index > not_correct_index - left_index) else (right_index, "found_bigger")


def get_dict_distance(route_coordinates : RouteCoordinates) -> dict[tuple[str, str], float]:
    d_distance = {}

    for stop_start_i, stop_end_i in zip(range(len(route_coordinates.stops) - 1), range(1, len(route_coordinates.stops))):
        stop_start = route_coordinates.stops[stop_start_i]
        stop_end = route_coordinates.stops[stop_end_i]
        distance = haversine((stop_start.lat, stop_start.lon), (stop_end.lat, stop_end.lon))
        d_distance[(stop_start.name, stop_end.name)] = 1.1 * distance
    return d_distance
def matrix_stop_times_norm(stop_times : list[StopTime]) -> np.ndarray:
    result = []
    for stop_time in stop_times:
        np_array = np.array(list(map(get_time_in_min, stop_time.time)))
        result.append(np_array)
    stop_times = np.array(result)
    return stop_times


def get_correct_indexes(indexes_where_maybe_correct_stops : np.ndarray, stop_times : np.ndarray) -> np.ndarray:
    norm_m = stop_times - stop_times[0, :]
    result = []

    for x in indexes_where_maybe_correct_stops.ravel():  # или arr.flatten()

        indexes_where_smaller = np.where(indexes_where_maybe_correct_stops < x)[0]
        indexes_where_bigger = np.where(indexes_where_maybe_correct_stops > x)[0]

        matrix_before_stops = norm_m[indexes_where_smaller]
        matrix_after_stops = norm_m[indexes_where_bigger]

        indexes_in_norm_m_smaller = set()
        if matrix_before_stops.size > 0:
            diff_smaller = matrix_before_stops - norm_m[x, :]
            mask_smaller = np.all(diff_smaller < 0, axis=1)
            indexes_in_norm_m_smaller = set(indexes_where_smaller[mask_smaller])

        indexes_in_norm_m_bigger = set()
        if matrix_after_stops.size > 0:
            diff_bigger = matrix_after_stops - norm_m[x, :]
            mask_bigger = np.all(diff_bigger > 0, axis=1)
            indexes_in_norm_m_bigger = set(indexes_where_bigger[mask_bigger])

        indexes_where_verification1_is_successful = (
            indexes_in_norm_m_smaller | indexes_in_norm_m_bigger
        )

        if len(indexes_where_verification1_is_successful) >= indexes_where_maybe_correct_stops.shape[0] / 2:
            result.append(x)
    return np.array(result)



def get_time_move_array(stop_times : np.ndarray) -> list[float]:
    norm_m = stop_times - stop_times[0, :]
    return list(norm_m.mean(axis=1))


def get_final_distance_between_stops(index_1, index_2, stop_times : list[StopTime], dict_distance: dict[tuple[str, str], float]):
    min_index = min(index_1, index_2)
    max_index = max(index_1, index_2)
    need_times = stop_times[min_index:max_index+1]
    distance = 0
    for stop_time_start, stop_time_end in zip(need_times[:-2], need_times[1:]):
        distance += dict_distance[(stop_time_start.stop_name, stop_time_end.stop_name)]
    return distance

