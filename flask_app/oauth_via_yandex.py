import json

import requests

import base64
from config.config import Config


def encode_base64(client_id, client_secret):
    stroka = str(client_id) + ':' + str(client_secret)
    encoded = (base64.b64encode(stroka.encode('ascii')))
    encoded_ascii = encoded.decode('ascii')
    print('encoded_ascii', encoded_ascii)
    return encoded_ascii


def get_code(request):

    state = request.args.get('state')
    print(state)

    url = 'https://oauth.yandex.ru'

    params = {
        # Content - Length:
        'content_type': 'application/x-www-form-urlencoded',
        'Authorization': encode_base64(Config.YAN_CLIENT_ID, Config.YAN_CLIENT_SECRET),
        'grant_type': 'authorization_code',
        'code': request.args.get('code'),
    }

    x = requests.get(url, params=params)
    print('STATUS_CODE: ', x.status_code)
    print("url:", url)
    print("params:", params)
