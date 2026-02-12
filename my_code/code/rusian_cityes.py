import asyncio
import requests
from googletrans import Translator
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def get_russian_cities_population(min_population):
    """Получает города России с населением больше min_population через Overpass API"""

    overpass_query = f"""
    [out:json][timeout:25];
    area["ISO3166-1"="RU"][admin_level=2];
    (
      node[place="city"](area);
      node[place="town"](area);
    );
    out body;
    """

    response = requests.post(
        "https://overpass-api.de/api/interpreter",
        data={'data': overpass_query},
    )
    print(response)
    cities = []
    for element in response.json()['elements']:
        tags = element.get('tags', {})
        population_str = tags.get('population', '0')

        try:
            # Обрабатываем разные форматы населения
            population = int(float(population_str)) if population_str else 0
        except (ValueError, TypeError):
            population = 0

        if population >= min_population:
            cities.append({
                'name': tags.get('name', 'Unknown'),
                'name:ru': tags.get('name:ru', ''),
                'population': population,
                'lat': element.get('lat'),
                'lon': element.get('lon'),
                'osm_id': element.get('id')
            })

    # Сортируем по населению (по убыванию)
    cities.sort(key=lambda x: x['population'], reverse=True)
    return cities


async def get_english_name_with_population(n):
    # Использование 500000
    cities = get_russian_cities_population(n)
    translator = Translator()
    cities_eng = []
    for city in cities:
        eng_name = await translator.translate("city " + city['name'], src='ru', dest='en')
        print(f"{eng_name.text}: {city['population']} жителей")
        a = {
            'name': eng_name.text[7:],
            'population': int(city['population']),
        }
        cities_eng.append(a)
    return cities_eng


def read_cities_file(filename):
    cities = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            # Разделяем строку на части
            parts = line.split(':')
            if len(parts) != 2:
                continue

            # Извлекаем название города
            city_part = parts[0].replace('city', '')[3:].strip()

            # Извлекаем население
            population_part = parts[1].replace('жителей', '').strip()

            try:
                population = int(population_part)
                cities.append({
                    "name": city_part,
                    "population": population
                })
            except ValueError:
                print(f"Ошибка преобразования населения для города: {city_part}")

    return cities



#filename = "cities.txt"
#cities_list = read_cities_file(filename)
#print(cities_list)


#asyncio.run(get_english_name_with_population(100000))
