from bs4 import BeautifulSoup

from my_code.code.transport.classes import Route, RouteTimes, SubRouteTimes, StopTime
from my_code.code.utilite import get_slow_query


def get_route_times_by_soup(name_route: str, soup : BeautifulSoup) -> SubRouteTimes:
    list_stops = soup.find(class_='bus-stops')
    stops = list_stops.find_all('row')
    stop_time = [] # StopTime
    for stop in stops:
        name_stop_content = str(stop.find('a').contents[0]) #text
        name_stop = name_stop_content[name_stop_content.find(')') + 1:].strip()
        times = map(lambda span: str(span.contents[0]), stop.find_all('span'))
        stop_time.append(StopTime(name_stop, list(times)))
    return SubRouteTimes(name_route, stop_time)




def get_route_times(name, url) -> RouteTimes:
    start_url = url + '/A' # адеемя, что всегда с A нумеруется
    s_start = get_slow_query(url, 15)
    l_start = s_start.find(class_='nav-pills')
    urls_object = l_start.find_all('a')
    url_routes = []
    name_routes = []
    for obj in urls_object:
        alpha_route = str(obj.get('href')).split('/')[-1]
        url_route = url + '/' + alpha_route
        name_sub_route = obj.contents[0]
        name_routes.append(name + ': ' + name_sub_route)
        url_routes.append(url_route)
    sub_route_times = [get_route_times_by_soup(name_routes[0], s_start)]
    for i in range(len(url_routes)):
        if url_routes[i] == start_url:
            continue
        soup = get_slow_query(url_routes[i], 15)
        sub_route_times.append(get_route_times_by_soup(name_routes[i], soup))
    return RouteTimes(name, sub_route_times)