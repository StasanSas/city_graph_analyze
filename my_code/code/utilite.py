import math
import os

from old_code.Modes.DefaultMode import DefaultMode
from old_code.Modes.PublicTransportMode import PublicTransportMode
from old_code.Modes.ScooterMode import ScooterMode
from old_code.Modes.WalkMode import WalkMode


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

# Использование
output_dir = "../city_polygons"
delete_empty_files(output_dir)