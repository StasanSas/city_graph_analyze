import requests
from bs4 import BeautifulSoup

url = "https://kudikina.ru/ekb/bus/"
response = requests.get(url)


if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    bus_items = soup.find_all(class_="bus-item")
    mar = []

    for i, item in enumerate(bus_items, 1):
        ref = item.get('href')
        mar.append(ref.split('/')[-1])
    print(mar)
else:
    print(f"Ошибка: {response.status_code}")