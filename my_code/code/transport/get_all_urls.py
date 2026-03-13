import asyncio
import os
from googletrans import Translator
from my_code.code.utilite import get_slow_query

base_url = 'https://kudikina.ru'

def get_city_and_city_url():
    d = {}
    soup_root = get_slow_query(base_url, 1)
    regions = soup_root.find(class_="block-regions")
    cities = soup_root.find(class_="block-cities")
    for city_object in cities.find_all('a'):
        r = city_object.get('href')
        name_city = city_object.find('span').contents[0]
        d[name_city] = base_url + r
    for obl in regions.find_all('a'):
        new_ref = base_url + obl.get('href')
        if new_ref == 'https://kudikina.ru/msk/' or new_ref == 'https://kudikina.ru/spb/':
            continue
        soup_obl = get_slow_query(new_ref, 1)
        cities = soup_obl.find(class_="cities")
        for city_object in cities.find_all('a'):
            r = city_object.get('href')
            name_city = city_object.find('span').contents[0]
            d[name_city] = base_url + r
    d['Москва'] = 'https://kudikina.ru/msk/'
    d['Санкт-Петербург'] = 'https://kudikina.ru/spb/'
    return d

path = '../city_transport_urls.txt'

def read_city_from_file():
    d = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            city, url = line.split('\t')
            d[city] = url[:-1]
    return d

def write_city_from_file(d):
    with open(path, 'w', encoding='utf-8') as f:
        for city, url in d.items():
            f.write(f'{city}\t{url}\n')

def get_cash_city():
    if not os.path.exists(path):
        d = get_city_and_city_url()
        write_city_from_file(d)
    return read_city_from_file()


async def get_d_by_rus_get_english():
    city_url = get_cash_city()
    d = {}
    translator = Translator()
    for city, url in city_url.items():
        result = await translator.translate('город ' + city, src='ru', dest='en')
        en_city = result.text.replace('city', '').replace('of', '').replace('​​ ', '').strip()
        d[city] = en_city
        print(en_city)
    return d

def get_cash_city_en_by_ru():
    path = '../city_en_by_ru.txt'
    if not os.path.exists(path):
        d = asyncio.run(get_d_by_rus_get_english())
        with open(path, 'w', encoding='utf-8') as f:
            for city_ru, city_en in d.items():
                f.write(f'{city_ru}\t{city_en}\n')
        return d
    else:
        d = {}
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                city_ru, city_en = line.split('\t')
                d[city_ru] = city_en[:-1]
        return d


print(get_cash_city_en_by_ru())
