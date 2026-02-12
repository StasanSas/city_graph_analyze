import statistics
from collections import defaultdict, Counter
import math

from old_code.Handler import OSMHandler


class OSMHandlerWithStats(OSMHandler):
    def __init__(self, start_ref, end_ref, mode='walk', file='city.osm.pbf'):
        super().__init__(start_ref, end_ref, mode=mode, file=file)
        self.edge_lengths = []  # Список всех длин рёбер
        self.way_lengths = []  # Длины ways
        self.edge_by_highway_type = defaultdict(list)
        # Словарь для хранения координат узлов
        self.node_coords = {}

    def node(self, n):
        """Сохраняем координаты узлов"""
        self.node_coords[n.id] = (n.location.lat, n.location.lon)

    def add_edge(self, u, v, data):
        """Добавляем ребро и вычисляем/собираем статистику"""

        # ВЫЧИСЛЯЕМ ДЛИНУ, если её нет в data
        if 'length' not in data:
            # Вычисляем длину по координатам узлов
            if u in self.node_coords and v in self.node_coords:
                lat1, lon1 = self.node_coords[u]
                lat2, lon2 = self.node_coords[v]
                length = self.calculate_distance(lat1, lon1, lat2, lon2)
                data['length'] = length
            else:
                # Если координат нет, используем 0 или пропускаем
                length = 0
                data['length'] = length
        else:
            length = data['length']

        # Собираем статистику
        self.edge_lengths.append(length)


    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Вычисляет расстояние между двумя точками в метрах (формула гаверсинусов)"""
        # Радиус Земли в метрах
        R = 6371000

        # Преобразуем градусы в радианы
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        # Формула гаверсинусов
        a = (math.sin(delta_phi / 2) * math.sin(delta_phi / 2) +
             math.cos(phi1) * math.cos(phi2) *
             math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def print_statistics(self):
        """Вывод статистики по длинам рёбер"""
        if not self.edge_lengths:
            print("Нет данных о рёбрах")
            return

        print("=== СТАТИСТИКА ПО ДЛИНАМ РЁБЕР ===")
        print(f"Общее количество рёбер: {len(self.edge_lengths)}")
        print(f"Минимальная длина: {min(self.edge_lengths):.2f} м")
        print(f"Максимальная длина: {max(self.edge_lengths):.2f} м")
        print(f"Средняя длина: {statistics.mean(self.edge_lengths):.2f} м")
        print(f"Медианная длина: {statistics.median(self.edge_lengths):.2f} м")

        # Стандартное отклонение (с проверкой)
        if len(self.edge_lengths) > 1:
            print(f"Стандартное отклонение: {statistics.stdev(self.edge_lengths):.2f} м")

        # Квартили
        sorted_lengths = sorted(self.edge_lengths)
        if sorted_lengths:
            q1_idx = len(sorted_lengths) // 4
            q3_idx = 3 * len(sorted_lengths) // 4
            q1 = sorted_lengths[q1_idx]
            q3 = sorted_lengths[q3_idx]
            print(f"Первый квартиль (Q1): {q1:.2f} м")
            print(f"Третий квартиль (Q3): {q3:.2f} м")
