import math
import os
import random
import time

import requests
from selenium.webdriver.common.by import By

import networkx as nx
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

from my_code.code.transport.classes import RouteTimes, RouteCoordinates
from old_code.Modes.DefaultMode import DefaultMode
from old_code.Modes.PublicTransportMode import PublicTransportMode
from old_code.Modes.ScooterMode import ScooterMode
from old_code.Modes.WalkMode import WalkMode

is_init_d = False
cash_coordinates = {} #('name_city', 'name_route') : (AnswerStop)
cash_time = {} #('name_city', 'name_route') : (RouteTimes)

driver = None
def delete_empty_files(directory):
    """Удаляет все пустые файлы в указанной директории"""
    deleted_count = 0

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # Проверяем, что это файл (не директория) и он пустой
        if os.path.isfile(filepath) and os.path.getsize(filepath) == 0:
            os.remove(filepath)
            print(f"Удален пустой файл: {filename}")
            deleted_count += 1

    print(f"Удалено пустых файлов: {deleted_count}")
    return deleted_count

def get_node_by_coords(value, graph):
    sorted_nodes = graph.get_sorted_nodes()
    low = 0
    high = len(sorted_nodes) - 1
    best_node = None
    best_distance = float('inf')

    while low <= high:
        mid = (low + high) // 2
        coords = graph.get_node_coords(sorted_nodes[mid])

        # Вычисляем расстояние между текущими координатами и искомыми
        distance = graph.haversine(coords, value)

        # Если нашли более близкий узел, обновляем best_node
        if distance < best_distance:
            best_distance = distance
            best_node = sorted_nodes[mid]

        # Сравниваем координаты для определения направления поиска
        if coords < value:
            low = mid + 1
        else:
            high = mid - 1

    return best_node

def get_time_in_min(s):
    split_str = s.split(':')
    return int(split_str[0]) * 60 + int(split_str[1])

def get_str_time(current_time):
    return f"{current_time // 60:02d}:{current_time % 60:02d}"

def get_mode_class(mode, file):
    if mode == 'walk':
        return WalkMode(file=file)
    elif mode == 'scooter':
        return ScooterMode(file=file)
    elif mode == 'PublicTransport':
        return PublicTransportMode(file=file)
    else:
        return DefaultMode(file=file)

def haversine(point_a, point_b):
    R = 6371.0

    lat_a, lon_a = math.radians(point_a[0]), math.radians(point_a[1])
    lat_b, lon_b = math.radians(point_b[0]), math.radians(point_b[1])

    dlat = lat_b - lat_a
    dlon = lon_b - lon_a

    a = (math.sin(dlat / 2) ** 2 +
     math.cos(lat_a) * math.cos(lat_b) * math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    distance = R * c
    return distance * 1000

def read_graphml(part_path : str) -> nx.Graph:
    path = os.path.join("../city_pedestrian_graph", part_path)
    print(os.path.abspath(path))
    if os.path.exists(path):
        return nx.read_graphml(path)
    else:
        path = os.path.join("../city_cleaned_graphs", part_path)
        return nx.read_graphml(path)


def write_graphml(graph : nx.Graph, part_path : str) -> None:
    base_path = "../city_cleaned_graphs"
    parts_path = part_path.split("/")
    if len(parts_path) != 2:
        raise Exception("Дай папку")
    if not os.path.isdir(os.path.join(base_path, parts_path[0])):
        raise Exception("Нет такой папки")
    path = os.path.join(base_path, part_path)
    nx.write_graphml(
        graph,
        path,
        encoding="utf-8",
        prettyprint=True
    )
# Использование
#output_dir = "../city_polygons"
#delete_empty_files(output_dir)


def get_slow_query(url, wait_time=10, max_retries=3, use_proxy=False, proxy=None):
    """
        Улучшенная версия с маскировкой fingerprint
        """
    # Список User-Agent для ротации
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    ]

    # Разные разрешения экрана
    RESOLUTIONS = [(1920, 1080), (1366, 768), (1440, 900), (1536, 864)]

    for attempt in range(max_retries):
        driver = None
        try:
            # Случайная задержка перед запросом
            delay = 2 + random.uniform(1, 3) * attempt
            time.sleep(delay)

            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")

            # Случайное разрешение
            width, height = random.choice(RESOLUTIONS)
            options.add_argument(f"--window-size={width},{height}")

            # Случайный User-Agent
            options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")

            # Отключаем автоматизацию
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            # Прокси если нужно
            if use_proxy and proxy:
                options.add_argument(f"--proxy-server={proxy}")

            driver = webdriver.Chrome(options=options)

            # Маскировка через CDP (самый мощный способ)
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                        // Прячем автоматизацию
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });

                        // Добавляем плагины
                        Object.defineProperty(navigator, 'plugins', {
                            get: () => [1, 2, 3, 4, 5]
                        });

                        // Добавляем языки
                        Object.defineProperty(navigator, 'languages', {
                            get: () => ['ru-RU', 'ru', 'en-US', 'en']
                        });

                        // Эмулируем Chrome
                        window.chrome = {
                            runtime: {}
                        };

                        // Прячем следы автоматизации в консоли
                        const originalQuery = window.navigator.permissions.query;
                        window.navigator.permissions.query = (parameters) => (
                            parameters.name === 'notifications' ?
                                Promise.resolve({ state: Notification.permission }) :
                                originalQuery(parameters)
                        );
                    """
            })

            driver.set_page_load_timeout(wait_time)
            driver.get(url)

            # Ждем загрузку
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Имитируем поведение человека
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(random.uniform(0.5, 1.5))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(0.5, 1.5))
            driver.execute_script("window.scrollTo(0, 0);")

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            # Проверяем не капча ли

            return soup

        except Exception as e:
            print(f"Попытка {attempt + 1} не удалась: {type(e).__name__}: {e}")

            if attempt == max_retries - 1:
                raise Exception(f"Не удалось получить {url} после {max_retries} попыток")

            # Экспоненциальная задержка между попытками
            time.sleep((2 ** attempt) + random.uniform(1, 3))

        finally:
            if driver:
                driver.quit()

    return None

def get_slow_query_bad(url, t):
    time.sleep(t)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        raise Exception(f"Ошибка: {url} - {response.status_code}")

def read_city_from_file(path):
    d = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split('\t')
            if len(parts) > 2:
                continue
            key, value = parts[0], parts[1]
            d[key] = value[:-1]
    return d

def write_city_from_file(path, d):
    with open(path, 'w', encoding='utf-8') as f:
        for key, value in d.items():
            f.write(f'{key}\t{value}\n')

def get_dictionary_abbreviations_city():
    path = "dictionary_abbreviations.txt"
    d = {}
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for l in lines:
            l = l.replace('\n', '')
            s, b = l.split(' ', 1)
            d[b] = s.lower()
    print(d)
    #get_dictionary_abbreviations_city()

def init_d():
    global cash_coordinates
    global cash_time
    global is_init_d
    if not is_init_d:
        coordinates_dir = '../transport/data_coordinates'
        for dir_city_name in os.listdir(coordinates_dir):
            dir_city_path = os.path.join(coordinates_dir, dir_city_name)
            for filename_route in os.listdir(dir_city_path):
                dir_route_path = os.path.join(dir_city_path, filename_route)
                route_name = filename_route.replace('.txt', '')
                with open(dir_route_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    answer_stop =  RouteCoordinates.from_json(content)
                    cash_coordinates[(dir_city_name, route_name)] = answer_stop

        time_dir = '../transport/data_time'

        for dir_city_name in os.listdir(time_dir):
            dir_city_path = os.path.join(time_dir, dir_city_name)
            for filename_route in os.listdir(dir_city_path):
                dir_route_path = os.path.join(dir_city_path, filename_route)
                route_name = filename_route.replace('.txt', '')
                with open(dir_route_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    route_times =  RouteTimes.from_json(content)
                    cash_time[(dir_city_name, route_name)] = route_times
        is_init_d = True
    return cash_coordinates, cash_time

def get_coordinates(name_city, name_route):
    cash_coordinates_l, _ = init_d()
    if (name_city, name_route) not in cash_coordinates_l:
        return None
    return cash_coordinates_l[(name_city, name_route)]


def get_time(name_city, name_route):
    _, cash_time_l = init_d()
    if (name_city, name_route) not in cash_time_l:
        return None
    return cash_time_l[(name_city, name_route)]









