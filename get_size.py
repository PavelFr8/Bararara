import requests


def get_size(address_ll, adr2):
    org_point = address_ll
    org_point2 = adr2

    params = {
        "ll": address_ll,
        "l": "map",
        "pt": "{},pm2dgl~{},pm2dgl".format(org_point, org_point2),
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=params)
    return response
