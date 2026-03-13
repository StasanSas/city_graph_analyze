import time

import requests
from bs4 import BeautifulSoup

from my_code.code.utilite import get_slow_query


def get_all_routes_bus():
    url = "https://kudikina.ru/ekb/bus/"
    response = requests.get(url)


    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        bus_items = soup.find_all(class_="bus-item")
        mar = []

        for i, item in enumerate(bus_items, 1):
            ref = item.get('href')
            mar.append(ref.split('/')[-1])
        return mar
    else:
        print(f"Ошибка: {response.status_code}")




def get_all_stops_bus(routes_bus_list_name):
    url = "https://kudikina.ru/ekb/bus/"
    stops = {} # name : [time]
    for routes_bus in routes_bus_list_name:
        soup = get_slow_query(url + routes_bus + "/A", 2)
        root = soup.find(class_="bus-stops")
        for stop_object in root.find_all(class_="row"):
            name_stop = str(stop_object.find(class_="bus-stop").find('a').contents[0])
            name_stop = name_stop.replace('\n', '').split(')')[1].strip()
            stops[name_stop] = routes_bus
            print(name_stop)
            stops_time_obj = stop_object.find(class_="stop-times").find_all('span')
            time_r = [str(time.contents[0]) for time in stops_time_obj if time.get('class') != 'show-all']
            print(time_r)

routes = get_all_routes_bus()
stops = get_all_stops_bus(routes)