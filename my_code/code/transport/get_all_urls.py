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
    print(d)

get_city_and_city_url()