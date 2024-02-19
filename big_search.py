import sys
from io import BytesIO
import requests
from PIL import Image
from get_size import get_size
import math
from buisness import find_buisness
'''
python big_search.py Москва, 4-й Вятский переулок

0.002, 0.002
'''


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000 # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return float(distance / 1000)


def big_search():
    toponym_to_find = " ".join(sys.argv[1:])

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]

    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    address_ll = ",".join([toponym_longitude, toponym_lattitude])

    way_to_point = find_buisness(address_ll, '0.005,0.005', 'аптека')
    address = way_to_point['properties']['CompanyMetaData']['address']
    name = way_to_point['properties']['CompanyMetaData']['name']
    coord = way_to_point['geometry']['coordinates']

    len_way = lonlat_distance((float(toponym_longitude), float(toponym_lattitude)),
                              coord)

    print(f'Название: {name}')
    print(f'Адрес: {address}')
    print(f'Путь до данной точкт: {round(len_way * 100, 1)}')

    response = get_size(",".join(map(str, coord)), address_ll)

    Image.open(BytesIO(
        response.content)).show()


big_search()
