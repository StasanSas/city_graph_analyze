import asyncio
import os
import subprocess
import time
import requests
from shapely import Polygon, Point, LineString, GeometryCollection
from shapely.geometry import shape, MultiPolygon

from my_code.code.rusian_cityes import read_cities_file

# Список городов с населением ≥500 000
cities = [
    #{"name": "Moscow", "population": 10381222},
    {"name": "Saint Petersburg", "population": 5028000},
    {"name": "Novosibirsk", "population": 1419007},
    {"name": "Yekaterinburg", "population": 1349772},
    {"name": "Nizhny Novgorod", "population": 1284164},
    {"name": "Kazan", "population": 1104738},
    {"name": "Chelyabinsk", "population": 1062919},
    {"name": "Omsk", "population": 1129281},
    {"name": "Samara", "population": 1134730},
    {"name": "Rostov-on-Don", "population": 1074482},
    {"name": "Ufa", "population": 1033338},
    {"name": "Krasnoyarsk", "population": 927200},
    {"name": "Voronezh", "population": 848752},
    {"name": "Volgograd", "population": 1011417},
    {"name": "Perm", "population": 982419},
    {"name": "Krasnodar", "population": 649851},
    {"name": "Ulyanovsk", "population": 640680},
    {"name": "Izhevsk", "population": 631038}
]

def get_city_geometry(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{city_name}, Russia",
        "format": "json",
        "polygon_geojson": 1,
        "limit": 1
    }
    headers = {"User-Agent": "stanislav.ivanov.2004@internet.ru"}
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def create_multipolygon_from_bbox(boundingbox):
    """
    Создает GeoJSON мультиполигон из boundingbox
    boundingbox: [south, north, west, east] - все значения как строки
    """
    try:
        south, north, west, east = map(float, boundingbox)

        multipolygon = {
            "type": "MultiPolygon",
            "coordinates": [[[
                [west, south],  # нижний левый
                [east, south],  # нижний правый
                [east, north],  # верхний правый
                [west, north],  # верхний левый
                [west, south]   # закрываем полигон
            ]]]
        }
        return multipolygon
    except (ValueError, TypeError, IndexError) as e:
        print(f"Error creating multipolygon from bbox {boundingbox}: {e}")
        return None


def save_to_poly(geojson, filename):
    geom = shape(geojson)
    with open(filename, 'w') as f:
        if isinstance(geom, Point):
            print("Предупреждение: Геометрия является точкой, нельзя создать полигон")
            return
        elif isinstance(geom, LineString):
            print("Предупреждение: Геометрия является линией, нельзя создать полигон")
            return
        elif isinstance(geom, GeometryCollection):
            print("Предупреждение: Геометрия является коллекцией, обработка не поддерживается")
            return
        f.write("city\n")
        polygon_count = 1
        for p in geom.geoms if isinstance(geom, MultiPolygon) else [geom]:
            if not isinstance(p, Polygon):
                print(f"Пропускаем не-полигональную геометрию: {type(p)}")
                continue
            f.write(f"{polygon_count}\n")

            for x, y in p.exterior.coords:
                f.write(f"    {x} {y}\n")
            f.write("END\n")

            # Внутренние кольца (дырки)
            for interior in p.interiors:
                f.write("!\n")  # Маркер для внутреннего кольца
                for x, y in interior.coords:
                    f.write(f"    {x} {y}\n")
                f.write("END\n")  # Закрываем внутреннее кольцо

            polygon_count += 1

        f.write("END\n")


def set_in_file_polygons_of_cities(cities):
    output_dir = "../city_polygons"
    os.makedirs(output_dir, exist_ok=True)

    for city in cities:
        filename = os.path.join(output_dir, f"{city['name'].replace(' ', '_')}.poly")
        if os.path.exists(filename):
            continue
        print(f"Processing {city['name']}...")
        geometry = get_city_geometry(city['name'])
        if geometry:
            geojson = geometry[0].get('geojson')
            if geojson.get("type") == "MultiPolygon":
                save_to_poly(geojson, filename)
                print(f"Saved {city['name']} polygon to {filename}")
            else:
                boundingbox = geometry[0].get('boundingbox')
                if boundingbox:
                    bbox_polygon = create_multipolygon_from_bbox(boundingbox)
                    save_to_poly(bbox_polygon, filename)
                    print(f"✓ Saved {city['name']} polygon (boundingbox) to {filename}")
                else:
                    print(f"✗ No geometry data for {city['name']}")
        time.sleep(1.5)  # Respect Nominatim usage policy


async def run_osmium_extract_async(filename, graph_filename):
    """Асинхронный запуск osmium"""
    process = await asyncio.create_subprocess_exec(
        "osmium", "extract", "-p", filename,
        "russia-251026.osm.pbf", "-o", graph_filename,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        print(f"Successfully processed {filename}")
    else:
        print(f"Error processing {filename}: {stderr.decode()}")

    return process.returncode


def run_osmium_extract(filename, graph_filename):
    """Синхронный запуск osmium"""
    try:
        # Запускаем процесс и ждем его завершения
        result = subprocess.run(
            ["osmium", "extract", "-p", filename, "russia-251026.osm.pbf", "-o", graph_filename],
            capture_output=True,
            text=True,
            check=True
        )

        print(f"Successfully processed {filename}")
        return 0

    except subprocess.CalledProcessError as e:
        print(f"Error processing {filename}: {e.stderr}")
        return e.returncode
    except FileNotFoundError:
        print("Error: osmium command not found. Make sure osmium is installed and in PATH")
        return 1
    except Exception as e:
        print(f"Unexpected error processing {filename}: {e}")
        return 1


async def set_in_file_graphs_of_cities(cities):
    output_dir = "../city_graphs"
    os.makedirs(output_dir, exist_ok=True)

    #tasks = []
    for city in cities:
        print(f"Processing graph: {city['name']}...")
        filename = f"./city_polygons/{city['name'].replace(' ', '_')}.poly"
        graph_filename = os.path.join(output_dir, f"{city['name'].replace(' ', '_')}_graph.osm.pbf")
        if os.path.exists(graph_filename):
            continue
        run_osmium_extract(filename, graph_filename)
        #tasks.append(task)

    #results = await asyncio.gather(*tasks, return_exceptions=True)

    #for city, result in zip(cities, results):
        #if isinstance(result, Exception):
            #print(f"Error with {city['name']}: {result}")
        #else:
            #print(f"Completed {city['name']} with code: {result}")

async def main():
    cities = read_cities_file('rusian_city.txt') #await get_english_name_with_population(100000)
    #set_in_file_polygons_of_cities(cities=cities)
    await set_in_file_graphs_of_cities(cities)

asyncio.run(main())
#data = get_city_geometry('Moscow') #Krasnodar
#formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
#print(formatted_json[:5000])

