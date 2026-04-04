import os
from datetime import datetime, timedelta, time

from my_code.code.algos.transport_routes.transport_routes import TransportRoute, DataArrival
from my_code.code.utilite import get_time_in_min, get_time_in_sec

DEFAULT_DURATION = 60 * 60 * 24
def parse_tuple(tup : str) -> (float, float):
    s_time_str, e_time_str = tup.split(',')
    time_s = get_time_in_sec(s_time_str)
    time_e = get_time_in_sec(e_time_str)
    return time_s, time_e

def get_smaller_d_data_time_arrival(d_old : dict[DataArrival, DataArrival], start : float = 0.0, duration : float = DEFAULT_DURATION) -> dict[DataArrival, DataArrival]:
    end = start + duration
    d_new = {}
    for s, e in d_old.items():
        if start <= s.arrival_time <= end:
            d_new[s] = e
    return d_new


def get_transport_routes(name_city, start_time = 0.0, duration = DEFAULT_DURATION) -> list[TransportRoute]:
    dir = f'../transport/result/{name_city}'
    if not os.path.exists(dir):
        raise Exception(f'{dir} не существует. Необходимо сделать загрузку')
    r = []
    for i, filename_route in enumerate(os.listdir(dir)):
        dir_route_path = os.path.join(dir, filename_route)
        route_name = filename_route.replace('.txt', '')
        d = {}
        with open(dir_route_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                start_id_str, stop_id_str, times = line.split('\t')
                start_id = int(start_id_str)
                stop_id = int(stop_id_str)
                times = times[1:-2]
                times_parsed = times.split('),(')
                date_times = map(parse_tuple, times_parsed)
                for date_time_s, date_time_e in date_times:
                    s = DataArrival(start_id, date_time_s)
                    e = DataArrival(stop_id, date_time_e)
                    d[s] = e
        smaller_d = get_smaller_d_data_time_arrival(d, start_time, duration)
        route = TransportRoute(i, route_name, smaller_d)
        r.append(route)
    return r
