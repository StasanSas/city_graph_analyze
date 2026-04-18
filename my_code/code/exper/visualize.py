import json
import math
import os

import folium
import networkx as nx

from my_code.code.algos.clusterization.Cluster import Cluster


def visualize_graph_on_map(graph,
                           lat_min, lat_max,
                           lon_min, lon_max,
                           output_file="graph_on_map.html",
                           include_edges=True):

    center_lat = (lat_min + lat_max) / 2
    center_lon = (lon_min + lon_max) / 2

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=15,
        tiles="OpenStreetMap"
    )

    nodes_in_square = []

    for node in graph.nodes():

        if isinstance(node, tuple) and len(node) == 2:
            lat, lon = node
        else:
            lon = graph.nodes[node]["x_coord"]
            lat = graph.nodes[node]["y_coord"]

        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            nodes_in_square.append((node, lat, lon))

    node_set = {n for n, _, _ in nodes_in_square}

    print("nodes:", len(nodes_in_square))

    # --- узлы ---
    for node, lat, lon in nodes_in_square:

        folium.CircleMarker(
            location=(lat, lon),
            radius=2,
            color="red",
            fill=True,
            fill_opacity=1,
            weight=1
        ).add_to(m)

    # --- рёбра ---
    if include_edges:

        edge_count = 0

        for u, v in graph.edges():

            if u in node_set and v in node_set:

                if isinstance(u, tuple):
                    lat1, lon1 = u
                    lat2, lon2 = v
                else:

                    lon1 = graph.nodes[u]["x_coord"]
                    lat1 = graph.nodes[u]["y_coord"]

                    lon2 = graph.nodes[v]["x_coord"]
                    lat2 = graph.nodes[v]["y_coord"]

                folium.PolyLine(
                    [(lat1, lon1), (lat2, lon2)],
                    color="blue",
                    weight=1,
                    opacity=0.7
                ).add_to(m)

                edge_count += 1

        print("edges:", edge_count)

    nodes_js = []

    for node, lat, lon in nodes_in_square:
        nodes_js.append({
            "id": str(node),
            "lat": lat,
            "lon": lon
        })

    nodes_json = json.dumps(nodes_js)

    from folium import Element
    map_name = m.get_name()

    js_code = f"""
    function initNearestNodeHandler() {{

        var map = {map_name};
        var nodes = {nodes_json};
        var markers = [];

        function distance(lat1, lon1, lat2, lon2) {{
            return Math.sqrt(
                Math.pow(lat1 - lat2, 2) +
                Math.pow(lon1 - lon2, 2)
            );
        }}

        function collectMarkers() {{
            map.eachLayer(function(layer) {{
                if (layer instanceof L.CircleMarker) {{
                    markers.push(layer);
                }}
            }});
        }}

        map.on('click', function(e) {{

            var clickLat = e.latlng.lat;
            var clickLon = e.latlng.lng;

            var minDist = Infinity;
            var closestNode = null;
            var closestIndex = -1;

            for (var i = 0; i < nodes.length; i++) {{
                var d = distance(
                    clickLat, clickLon,
                    nodes[i].lat, nodes[i].lon
                );

                if (d < minDist) {{
                    minDist = d;
                    closestNode = nodes[i];
                    closestIndex = i;
                }}
            }}

            if (!closestNode) return;

            // сброс радиусов
            markers.forEach(function(m) {{
                m.setRadius(2);
            }});

            // выделение ближайшего
            if (markers[closestIndex]) {{
                markers[closestIndex].setRadius(8);
            }}

            // popup
            L.popup()
                .setLatLng(e.latlng)
                .setContent("Nearest node ID: " + closestNode.id)
                .openOn(map);

        }});

        collectMarkers();
    }}

    // Ждём, пока folium создаст карту
    setTimeout(initNearestNodeHandler, 1000);
    """

    m.get_root().script.add_child(Element(js_code))
    m.save(output_file)


    print("saved:", output_file)

    return output_file

import random

def visualize_clusters_on_map(graph,
                              clusters: list[Cluster],
                              lat_min, lat_max,
                              lon_min, lon_max,
                              output_file="clusters_map.html",
                              draw_connections=True):

    center_lat = (lat_min + lat_max) / 2
    center_lon = (lon_min + lon_max) / 2

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=15,
        tiles="OpenStreetMap"
    )

    def get_node_coords(node):
        if isinstance(node, tuple):
            return node
        else:
            lon = graph.nodes[str(node)]["x_coord"]
            lat = graph.nodes[str(node)]["y_coord"]
            return lat, lon

    def random_color():
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))
    c_cluster = 0
    c_nodes = 0
    for cluster in clusters:

        if not cluster.nodes:
            continue

        color = random_color()

        # --- центр ---
        center_latlon = get_node_coords(cluster.center)
        lat, lon = center_latlon
        if not (lat_min <= lat <= lat_max and lon_min <= lon <= lon_max):
            continue

        folium.CircleMarker(
            location=center_latlon,
            radius=6,
            color=color,
            fill=True,
            fill_opacity=1,
            weight=2
        ).add_to(m)
        c_cluster += 1
        c_nodes += 1

        # --- ноды ---
        for node in cluster.nodes:

            lat, lon = get_node_coords(node)

            if not (lat_min <= lat <= lat_max and lon_min <= lon <= lon_max):
                continue
            c_nodes += 1
            folium.CircleMarker(
                location=(lat, lon),
                radius=3,
                color=color,
                fill=True,
                fill_opacity=0.8,
                weight=1
            ).add_to(m)

            # --- связь с центром ---
            if draw_connections:
                folium.PolyLine(
                    [center_latlon, (lat, lon)],
                    color=color,
                    weight=1,
                    opacity=0.5
                ).add_to(m)

    m.save(output_file)
    print(f"clusters saved: {output_file}\nКол-во кластеров: {c_cluster}\nКол-во вершин: {c_nodes}")

    return output_file

def get_sizes_for_draw(center_lat, center_lon, radius_km):
    # Примерное преобразование: 1 градус широты ≈ 111 км # 1 градус долготы ≈ 111 * cos(широта) км
    scale_lon = math.cos(math.radians(center_lon))
    lat_delta = radius_km / 111.32
    lon_delta = radius_km / (111.32 * scale_lon)
    lat_min = center_lat - lat_delta
    lat_max = center_lat + lat_delta
    lon_min = center_lon - lon_delta
    lon_max = center_lon + lon_delta
    print(f"Поиск в области радиусом {radius_km} км вокруг ({center_lat:.5f}, {center_lon:.5f})")
    print(f"Границы: lat [{lat_min:.5f}, {lat_max:.5f}], lon [{lon_min:.5f}, {lon_max:.5f}]")
    return lat_min, lat_max, lon_min, lon_max

def find_and_visualize_area(graph, center_lat, center_lon, radius_km=0.9):
    lat_min, lat_max, lon_min, lon_max = get_sizes_for_draw(center_lat, center_lon, radius_km)
    return visualize_graph_on_map(graph, lat_min, lat_max, lon_min, lon_max, output_file=f"area_{radius_km}km.html")

def find_and_visualize_clusters_in_ares(graph, clusters : list[Cluster], center_lat, center_lon, size_cluster, name_city, radius_km=0.9):
    lat_min, lat_max, lon_min, lon_max = get_sizes_for_draw(center_lat, center_lon, radius_km)
    return visualize_clusters_on_map(graph, clusters, lat_min, lat_max, lon_min, lon_max, output_file=f"size_{size_cluster}_area_{name_city}_{radius_km}km.html")
# Пример использования:
def main():
    from old_code.Handler import OSMHandler

    # Ваши данные
    start_ref = (55.63265, 37.65817)
    end_ref = (55.8468, 37.44116)
    mode = 'walk'
    file = 'C:/Users/stanislav.ivanov/Desktop/city_graph_analyze/my_code/city_cleaned_graphs/one_component__and__without_2_chains/Ekaterinburg.graphml'
    g = nx.read_graphml(file)

    # Вариант 1: Задать квадрат вручную
    # Центр Екатеринбурга примерно: 56.8380, 60.5973
    #square_file = visualize_square_html(
    #    graph=g,
    #    lat_min=56.835,  # Южная граница
    #    lat_max=56.84,  # Северная граница
    #    lon_min=60.59,  # Западная граница
    #    lon_max=60.60,  # Восточная граница
    #    output_file="ekaterinburg_square.html",
    #    include_edges=True,
    #    max_nodes=50000  # Ограничим для производительности
    #)

    # Вариант 2: Найти область вокруг точки
    area_file = find_and_visualize_area(
        graph=g,
        center_lat=56.88847736123229,  # Центр Екатеринбурга
        center_lon=60.613608756368535,
        radius_km=1.5  # 2 км радиус
    )

    print("\nДля открытия визуализации:")


if __name__ == "__main__":
    main()