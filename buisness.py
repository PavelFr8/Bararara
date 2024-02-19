import requests
from geocoder import get_nearest_object


def find_buisnesses(ll, spn, text, locate='ru_RU'):
    search = 'https://search-maps.yandex.ru/v1/'

    params = {
        'apikey': 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
        'text': text,
        'lang': locate,
        'spn': spn,
        'll': ll,
        'type': 'biz'
    }

    response = requests.get(search, params=params)

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
                request=search, status=response.status_code, reason=response.reason))

    json_response = response.json()
    organizations = json_response['features']
    return organizations


def find_buisness(ll, spn, text, locate='ru_RU'):
    orgs = find_buisnesses(ll, spn, text, locate)
    if len(orgs):
        return orgs[0]



