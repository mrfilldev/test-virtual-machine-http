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

    headers = {
        'Authorization': encode_base64(Config.YAN_CLIENT_ID, Config.YAN_CLIENT_SECRET),
    }

    params = {
        # Content - Length:
        #'content_type': 'application/x-www-form-urlencoded',
        'grant_type': 'authorization_code',
        'code': request.args.get('code'),
    }

    response = requests.post(url, params=params, headers=headers)
    print('STATUS_CODE: ', response.status_code)
    print("url:", url)
    print("params:", params)

    print('\nresponse: ', response)
    print('\nresponse.content: ', response.content)





