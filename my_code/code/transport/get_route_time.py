import os
from typing import List

from bs4 import BeautifulSoup

from my_code.code.transport.classes import Route, RouteTimes, SubRouteTimes, StopTime
from my_code.code.utilite import get_slow_query, get_time


def get_route_times_by_soup(name_route: str, soup : BeautifulSoup, name : str) -> SubRouteTimes:
    list_stops = soup.find(class_='bus-stops')
    stops = list_stops.find_all(class_='row')
    stop_times = [] # StopTime
    for stop in stops:
        name_stop_content = str(stop.find('a').contents[0]) #text
        name_stop = name_stop_content[name_stop_content.find(')') + 1:].strip()
        stop_time = process_time(name_stop, stop, name)
        stop_times.append(stop_time)
    return SubRouteTimes(name_route, stop_times)

def process_time(name_stop, soup_row, name) -> StopTime:
    interval_time = soup_row.find(class_='interval-times')
    stop_times = soup_row.find(class_='stop-times')
    if stop_times is not None:
        times = map(lambda span: str(span.contents[0]), soup_row.find_all('span'))
        times = filter(lambda time: time != "Показать все", times)
        return StopTime(name_stop, list(times))
    if interval_time is not None:
        interval_delta = soup_row.find(class_='interval-delta')
        interval_values_obj = interval_time.find_all('span')
        interval_values = list(map(lambda span: str(span.contents[0]), interval_values_obj))
        if len(interval_values) != 2:
            raise Exception(f'Непредвиденный интервал {name_stop}')

        small_time_intervals = interval_delta.find('thead').find_all('th')
        small_intervals = list(map(lambda span: str(span.contents[0]).split(' - '), small_time_intervals))
        #
        deltas_obj = interval_delta.find('tbody').find_all('td')
        deltas = list(map(lambda delta: str(delta.contents[0]), deltas_obj))
        converted_deltas = []
        for delta in deltas:
            delta_s = delta.split(' ')
            if len(delta_s) != 2 or delta_s[1] != 'мин':
                raise Exception(f'Непредвиденный формат дельты {name_stop}')
            converted_deltas.append(delta_s[0])
        times = convert_intervals_and_deltas_in_time_stop(small_intervals, converted_deltas)
        return StopTime(name_stop.title(), times)
    else:
        raise Exception(f'Не нашли времени {name_stop} в маршруте {name}')


def convert_intervals_and_deltas_in_time_stop(small_intervals, deltas) -> List[str]: # времена в виде строки
    current_time = None
    result = []
    for i in range(len(small_intervals)):
        small_interval = small_intervals[i]
        start_time_parts = small_interval[0].split(':')
        start_time = int(start_time_parts[0]) * 60 + int(start_time_parts[1])
        end_time_parts = small_interval[1].split(':')
        end_time = int(end_time_parts[0]) * 60 + int(end_time_parts[1])
        current_time = start_time if current_time is None else current_time

        delta = int(deltas[i])
        delta = delta if delta > 4 else 5

        while (current_time <= end_time):
            time_str_for_add = f"{current_time // 60:02d}:{current_time % 60:02d}"
            result.append(time_str_for_add)
            current_time += delta
    return result


def get_route_times(name, url) -> RouteTimes:
    start_url = url + '/A' # адеемя, что всегда с A нумеруется
    s_start = get_slow_query(start_url, 15)
    l_start = s_start.find(class_='nav-pills')
    urls_object = l_start.find_all('a')
    url_routes = []
    name_routes = []
    for obj in urls_object:
        alpha_route = str(obj.get('href')).split('/')[-1]
        url_route = url + '/' + alpha_route
        name_sub_route = str(obj.contents[0]).replace('\n', '')
        name_sub_route = name_sub_route[name_sub_route.find(')') + 1:].strip()
        name_routes.append(name + ': ' + name_sub_route)
        url_routes.append(url_route)
    sub_route_times = [get_route_times_by_soup(name_routes[0], s_start, name)]
    for i in range(len(url_routes)):
        if url_routes[i] == start_url:
            continue
        soup = get_slow_query(url_routes[i], 15)
        sub_route_times.append(get_route_times_by_soup(name_routes[i], soup, name))
    return RouteTimes(name, sub_route_times)

def get_cashed_route_times(name_city, name, ref) -> RouteTimes:
    path = f"../transport/data_time/{name_city}/{name}.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if get_time(name_city, name) is None:
        route_time = get_route_times(name, ref)
        with open(path, 'w', encoding='utf-8') as file:
            file.write(f'{route_time.to_json(ensure_ascii=False, indent=2)}')
        return route_time
    else:
        return get_time(name_city, name)