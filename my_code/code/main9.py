from my_code.code.algos.statistics.read_and_save import save, load
import folium
import math
from folium import plugins
import time
from my_code.code.utilite import read_graphml
s = load('Ну, базовая статистика')
print(s.config)
print(s.mean_statistic.get_mean() // 60)
print(s.statistic_percentile.get_percentile(0.25) // 60)
print(s.statistic_percentile.get_percentile(0.5) // 60)
print(s.statistic_percentile.get_percentile(0.75) // 60)
print(s.statistic_percentile.get_percentile(0.95) // 60)

path = "time_pedestrian_graph/Ekaterinburg.graphml"
g = read_graphml(path)

from branca.colormap import LinearColormap
max_ = s.mean_statistic.get_mean()
def build_colormap(values):
    return LinearColormap(
        colors=["green", "yellow", "red"],
        vmin=min(values),
        vmax= (1.5 * sum(values)) / len(values),
    )

def visualize_node_colors(graph, stat_means, center_lat, center_lon, radius_km=10, output="nodes_map.html"):
    lat_delta = radius_km / 111.32
    lon_delta = radius_km / (2 * 111.32 * math.cos(math.radians(center_lat)))

    lat_min, lat_max = center_lat - lat_delta, center_lat + lat_delta
    lon_min, lon_max = center_lon - lon_delta, center_lon + lon_delta

    points = []

    # 1. собираем значения
    for node in graph.nodes():
        lon = graph.nodes[node]["x_coord"]
        lat = graph.nodes[node]["y_coord"]

        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            value = stat_means.get_mean(node)
            points.append((node, lat, lon, value))

    if not points:
        print("Нет точек в зоне")
        return

    values = [p[3] for p in points]
    colormap = build_colormap(values)

    # 2. карта
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14)

    # 3. рисуем вершины
    for node, lat, lon, value in points:
        color = colormap(value)

        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=f"node={node}, value={value:.2f}"
        ).add_to(m)

    colormap.caption = "Mean value"
    colormap.add_to(m)

    m.save(output)
    print(f"Сохранено {len(points)} узлов в {output}")

# Использование:
s_time = time.time()
visualize_node_colors(g, s.statistic_means_for_nodes, 56.8380, 60.5973, radius_km=20)
print(time.time() - s_time)