import os

import requests
from bs4 import BeautifulSoup

from my_code.code.utilite import get_slow_query, write_city_from_file, read_city_from_file


def get_all_names_route_and_ref(url, name) -> dict[str, str]:
    path = f"../transport/source_url/{name}_names_routes.txt"
    d = {}
    if not os.path.exists(path):
        s = get_slow_query(url, 1)
        types_route_object = s.find(class_="nav-pills").find_all('a')
        new_refs = []
        for types_object in types_route_object:
            part_ref = types_object.get('href')
            part_ref = part_ref.split('/')[-2]
            if types_object.contents[0] not in ['Остановки', 'Закрытые маршруты']:
                new_refs.append(url + part_ref + '/')

        for new_ref in new_refs:
            s = get_slow_query(new_ref, 1)
            route_objects = s.find(class_='text-center').find_all(class_='bus-item')
            for route_object in route_objects:
                href_route_parts = route_object.get('href').split('/')
                href_route = href_route_parts[2] + "/" + href_route_parts[3]
                name = route_object.contents[0].replace('\"', '').strip()
                d[name] = url + href_route

        write_city_from_file(path, d)
    d = read_city_from_file(path)
    return d

def set_process_source(name_city, url):
    path = f"../transport/source_url/{name_city}_names_routes.txt"
    if os.path.exists(path):
        temp_file = f"../transport/source_url/{name_city}_names_routes.txt" + '.tmp'

        with open(path, 'r', encoding='utf-8') as read_file:
            with open(temp_file, 'w', encoding='utf-8') as write_file:
                for line in read_file:
                    if line.endswith(url + '\n'):
                        write_file.write(line.replace('\n', '') + '\tprocessed\n')
                    else:
                        write_file.write(line)

        # Заменяем оригинал временным файлом
        os.remove(path)
        os.rename(temp_file, path)
    else:
        raise Exception("Нету файла источников для города")

