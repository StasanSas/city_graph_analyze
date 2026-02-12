import os


def visualize_square_html(graph,
                          lat_min, lat_max,
                          lon_min, lon_max,
                          output_file="square_graph.html",
                          include_edges=True,
                          max_nodes=None):
    """
    Визуализация всех вершин и рёбер в заданном географическом квадрате.

    Args:
        graph: NetworkX граф
        lat_min, lat_max: минимальная и максимальная широта
        lon_min, lon_max: минимальная и максимальная долгота
        output_file: имя выходного HTML файла
        include_edges: включать ли рёбра в визуализацию
        max_nodes: максимальное количество узлов (None = все)
    """
    print(f"Визуализация квадрата: lat [{lat_min:.4f}, {lat_max:.4f}], lon [{lon_min:.4f}, {lon_max:.4f}]")

    from pyvis.network import Network
    import os

    # Собираем узлы в квадрате
    nodes_in_square = []
    nodes_data = []  # Будут хранить (node, lat, lon)

    for node in graph.nodes():
        if isinstance(node, tuple) and len(node) == 2:
            lat, lon = node
            if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                nodes_in_square.append(node)
                nodes_data.append((node, lat, lon))

    if not nodes_in_square:
        print("Нет узлов в указанном квадрате")
        return None

    # Ограничиваем количество узлов если нужно
    if max_nodes and len(nodes_in_square) > max_nodes:
        import random
        nodes_data = random.sample(nodes_data, max_nodes)
        nodes_in_square = [node for node, _, _ in nodes_data]
        print(f"Ограничено до {max_nodes} узлов")

    print(f"Найдено узлов в квадрате: {len(nodes_in_square)}")

    # Создаём сеть PyVis
    net = Network(height="800px", width="100%",
                  bgcolor="#ffffff", font_color="black",
                  notebook=False)

    # Добавляем узлы с позиционированием по реальным координатам
    for node, lat, lon in nodes_data:
        # Преобразуем географические координаты в координаты экрана
        # В PyVis координаты идут от 0 до 1000
        x = ((lon - lon_min) / (lon_max - lon_min)) * 1000
        y = ((lat_max - lat) / (lat_max - lat_min)) * 1000  # Инвертируем Y

        net.add_node(str(node),
                     x=x,
                     y=y,
                     size=3,
                     color="#FF6B6B",  # Красный для выделения
                     shape="dot")

    # Добавляем рёбра, если нужно
    edges_in_square = []
    if include_edges:
        edges_in_square = []
        for u, v in graph.edges():
            if u in nodes_in_square and v in nodes_in_square:
                edges_in_square.append((u, v))

        print(f"Найдено рёбер в квадрате: {len(edges_in_square)}")

        # Добавляем рёбра
        edge_count = 0
        for u, v in edges_in_square:
            net.add_edge(str(u), str(v),
                         width=1.0,
                         color="#4285F4",  # Синий для рёбер
                         opacity=0.7)
            edge_count += 1

    # Отключаем физику для сохранения географического расположения
    net.toggle_physics(False)

    # Настройки визуализации
    net.set_options("""
    var options = {
      "nodes": {
        "shape": "circle",
        "size": 2,
        "font": {
          "size": 0,
          "face": "Arial"
        }
      },
      "edges": {
        "width": 1,
        "color": {
          "inherit": false
        },
        "smooth": {
          "type": "continuous",
          "forceDirection": "none"
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 200,
        "hideEdgesOnDrag": false,
        "hideNodesOnDrag": false
      },
      "physics": {
        "enabled": false,
        "stabilization": {
          "enabled": true,
          "iterations": 100
        }
      }
    }
    """)

    # Сохраняем HTML файл
    net.save_graph(output_file)

    # Также создаём HTML с картой и информацией
    create_square_info_html(graph, lat_min, lat_max, lon_min, lon_max,
                            nodes_in_square, edges_in_square if include_edges else [],
                            output_file)

    print(f"HTML файл сохранен: {os.path.abspath(output_file)}")
    print(f"Сводная страница создана: square_info.html")

    return output_file


def create_square_info_html(graph, lat_min, lat_max, lon_min, lon_max,
                            nodes_in_square, edges_in_square, original_file):
    """
    Создание информационной страницы с картой и статистикой.
    """
    import folium
    from folium.plugins import MarkerCluster, HeatMap
    import webbrowser
    from pathlib import Path

    # Создаём карту Folium
    center_lat = (lat_min + lat_max) / 2
    center_lon = (lon_min + lon_max) / 2

    m = folium.Map(location=[center_lat, center_lon],
                   zoom_start=14,
                   tiles='OpenStreetMap')

    # Добавляем прямоугольник квадрата
    square_coords = [
        [lat_min, lon_min],
        [lat_max, lon_min],
        [lat_max, lon_max],
        [lat_min, lon_max],
        [lat_min, lon_min]
    ]

    folium.Polygon(
        locations=square_coords,
        color='red',
        weight=2,
        fill=True,
        fill_color='red',
        fill_opacity=0.1
    ).add_to(m)


    # Сохраняем карту
    map_file = "square_map.html"
    m.save(map_file)

    # Создаём информационную страницу
    info_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Визуализация географического квадрата</title>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #eee;
            }}
            .grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }}
            .card {{
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 1px 5px rgba(0,0,0,0.1);
            }}
            .stats {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 10px;
            }}
            .stat-item {{
                margin: 10px 0;
                padding: 10px;
                background: rgba(255,255,255,0.1);
                border-radius: 5px;
            }}
            iframe {{
                width: 100%;
                height: 500px;
                border: 2px solid #ddd;
                border-radius: 5px;
            }}
            .coordinate-info {{
                background: #e3f2fd;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background: #4285F4;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 10px 5px;
                font-weight: bold;
            }}
            .button:hover {{
                background: #3367D6;
            }}
            .tab {{
                overflow: hidden;
                border-bottom: 1px solid #ccc;
                margin-bottom: 20px;
            }}
            .tab button {{
                background-color: inherit;
                float: left;
                border: none;
                outline: none;
                cursor: pointer;
                padding: 14px 16px;
                transition: 0.3s;
                font-size: 16px;
            }}
            .tab button:hover {{
                background-color: #ddd;
            }}
            .tab button.active {{
                background-color: #4285F4;
                color: white;
            }}
            .tabcontent {{
                display: none;
                padding: 20px;
                animation: fadeEffect 1s;
            }}
            @keyframes fadeEffect {{
                from {{opacity: 0;}}
                to {{opacity: 1;}}
            }}
            .node-list {{
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                padding: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Визуализация географического квадрата</h1>
                <p>Анализ узлов и рёбер в заданной области</p>
            </div>

            <div class="grid">
                <div class="card">
                    <h2>Интерактивный граф</h2>
                    <p>Наведите на узел для просмотра координат</p>
                    <iframe src="{original_file}"></iframe>
                    <div style="text-align: center; margin-top: 10px;">
                        <a href="{original_file}" target="_blank" class="button">Открыть в полном окне</a>
                    </div>
                </div>

                <div class="card">
                    <h2>Географическая карта</h2>
                    <p>Красная область - выбранный квадрат</p>
                    <iframe src="{map_file}"></iframe>
                    <div style="text-align: center; margin-top: 10px;">
                        <a href="{map_file}" target="_blank" class="button">Открыть карту отдельно</a>
                    </div>
                </div>
            </div>

            <div class="stats">
                <h2 style="color: white; margin-top: 0;">Статистика</h2>

                <div class="stat-item">
                    <strong>Географические границы:</strong><br>
                    Широта: {lat_min:.5f} → {lat_max:.5f}<br>
                    Долгота: {lon_min:.5f} → {lon_max:.5f}
                </div>

                <div class="stat-item">
                    <strong>Центр области:</strong><br>
                    Широта: {center_lat:.5f}<br>
                    Долгота: {center_lon:.5f}
                </div>

                <div class="stat-item">
                    <strong>Найдено узлов:</strong> {len(nodes_in_square)}
                </div>

                <div class="stat-item">
                    <strong>Найдено рёбер:</strong> {len(edges_in_square)}
                </div>

                <div class="stat-item">
                    <strong>Плотность графа в квадрате:</strong><br>
                    {len(edges_in_square) / max(1, len(nodes_in_square)):.2f} рёбер/узел
                </div>
            </div>

            <div class="tab">
                <button class="tablink" onclick="openTab(event, 'Nodes')">Узлы ({len(nodes_in_square)})</button>
                <button class="tablink" onclick="openTab(event, 'Edges')">Рёбра ({len(edges_in_square)})</button>
                <button class="tablink" onclick="openTab(event, 'Area')">Площадь области</button>
            </div>

            <div id="Nodes" class="tabcontent">
                <h3>Узлы в квадрате</h3>
                <div class="node-list">
                    {"<br>".join(str(node)[:50] for node in nodes_in_square[:200])}
                    {f"<br>... и ещё {len(nodes_in_square) - 200} узлов" if len(nodes_in_square) > 200 else ""}
                </div>
            </div>

            <div id="Edges" class="tabcontent">
                <h3>Рёбра в квадрате</h3>
                <div class="node-list">
                    {"<br>".join(f"{u} → {v}" for u, v in edges_in_square[:200])}
                    {f"<br>... и ещё {len(edges_in_square) - 200} рёбер" if len(edges_in_square) > 200 else ""}
                </div>
            </div>

            <div id="Area" class="tabcontent">
                <h3>Информация о площади</h3>
                <p>Приблизительные размеры области:</p>
                <ul>
                    <li>Ширина по долготе: {(lon_max - lon_min) * 111.32:.2f} км (на широте {center_lat:.1f}°)</li>
                    <li>Высота по широте: {(lat_max - lat_min) * 111.32:.2f} км</li>
                    <li>Приблизительная площадь: {((lon_max - lon_min) * 111.32 * (lat_max - lat_min) * 111.32):.2f} км²</li>
                </ul>
            </div>
        </div>

        <script>
            function openTab(evt, tabName) {{
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tabcontent");
                for (i = 0; i < tabcontent.length; i++) {{
                    tabcontent[i].style.display = "none";
                }}
                tablinks = document.getElementsByClassName("tablink");
                for (i = 0; i < tablinks.length; i++) {{
                    tablinks[i].className = tablinks[i].className.replace(" active", "");
                }}
                document.getElementById(tabName).style.display = "block";
                evt.currentTarget.className += " active";
            }}

            // По умолчанию открываем первую вкладку
            document.getElementsByClassName("tablink")[0].click();
        </script>
    </body>
    </html>
    """

    with open("square_info.html", "w", encoding="utf-8") as f:
        f.write(info_html)

    return "square_info.html"


def find_and_visualize_area(graph, center_lat, center_lon, radius_km=1):
    """
    Найти и визуализировать область вокруг заданной точки.

    Args:
        graph: NetworkX граф
        center_lat, center_lon: центр области
        radius_km: радиус в километрах
    """
    # Примерное преобразование: 1 градус широты ≈ 111 км
    # 1 градус долготы ≈ 111 * cos(широта) км
    lat_delta = radius_km / 111.32
    lon_delta = radius_km / (111.32)

    lat_min = center_lat - lat_delta
    lat_max = center_lat + lat_delta
    lon_min = center_lon - lon_delta
    lon_max = center_lon + lon_delta

    print(f"Поиск в области радиусом {radius_km} км вокруг ({center_lat:.5f}, {center_lon:.5f})")
    print(f"Границы: lat [{lat_min:.5f}, {lat_max:.5f}], lon [{lon_min:.5f}, {lon_max:.5f}]")

    return visualize_square_html(graph, lat_min, lat_max, lon_min, lon_max,
                                 output_file=f"area_{radius_km}km.html")


# Пример использования:
def main():
    from old_code.Handler import OSMHandler

    # Ваши данные
    start_ref = (55.63265, 37.65817)
    end_ref = (55.8468, 37.44116)
    mode = 'walk'
    file = '/my_code/city_graphs/Ekaterinburg_graph.osm.pbf'

    handler = OSMHandler(start_ref, end_ref, mode=mode, file=file)
    g = handler.graph.get_graph()

    print(f"Загружен граф: {g.number_of_nodes()} узлов, {g.number_of_edges()} рёбер")

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
        center_lat=56.8380,  # Центр Екатеринбурга
        center_lon=60.5973,
        radius_km=1  # 2 км радиус
    )

    print("\nДля открытия визуализации:")
    print(f"1. Откройте файл: {os.path.abspath(area_file)}")
    print(f"2. Или откройте файл: square_info.html")


if __name__ == "__main__":
    main()