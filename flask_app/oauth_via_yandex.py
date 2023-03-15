import json

import requests

import base64
from config.config import Config


def encode_base64(client_id, client_secret):
    stroka = str(client_id) + ':' + str(client_secret)
    encoded = base64.b64encode(stroka.encode("UTF-8"))
    return encoded.decode("UTF-8")


def get_code(request):

    state = request.args.get('state')
    print(state)

    url = 'https://oauth.yandex.ru/token'

    code = encode_base64(Config.YAN_CLIENT_ID, Config.YAN_CLIENT_SECRET)
    print('code: ', code)
    headers = {
        'Authorization': 'Basic ' + encode_base64(Config.YAN_CLIENT_ID, Config.YAN_CLIENT_SECRET),
    }

    params = {
        'grant_type': 'authorization_code',
        'code': request.args.get('code'),
    }

    response = requests.post(url, data=params, headers=headers)
    print('STATUS_CODE: ', response.status_code)
    print("url:", url)
    print("params:", params)

    print('\nresponse: ', response)
    print('\nresponse.content: ', response.content)


#
# curl -v -X POST 'https://oauth.yandex.ru/token' \
# -H 'Content-type: application/x-www-form-urlencoded' \
# -H 'Authorization: Basic MGM1NDZjZmFhNGU4NDBjNGI0MWJjYTRhOGFmMmU1NmE6Y2UxMGIxZjU0MTQxNGJhOWEwYmYzMTM5ZDBkZjlmNDk=' \
# -d 'grant_type=authorization_code&code=6678635'
