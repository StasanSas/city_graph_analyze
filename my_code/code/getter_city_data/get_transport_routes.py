import os
from datetime import datetime, timedelta

from my_code.code.algos.transport_routes.transport_routes import TransportRoute, DataArrival
from my_code.code.utilite import get_time_in_min


def parse_tuple(tup : str) -> (datetime, datetime):
    s_time_str, e_time_str = tup.split(',')
    time_s = get_time_in_min(s_time_str)
    time_e = get_time_in_min(e_time_str)

    date_time_s = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) \
         + timedelta(minutes=time_s)

    date_time_e = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) \
         + timedelta(minutes=time_e)
    return date_time_s, date_time_e


def get_transport_routes(name_city) -> list[TransportRoute]:
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
        route = TransportRoute(i, route_name, d)
        r.append(route)
    return r