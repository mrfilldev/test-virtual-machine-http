import json
import requests
import base64
from ..configuration.config import Config


def encode_base64(client_id, client_secret):
    stroka = str(client_id) + ':' + str(client_secret)
    encoded = base64.b64encode(stroka.encode("UTF-8"))
    return encoded.decode("UTF-8")


def get_code(request):
    # state = request.args.get('state')
    # name = request.args.get('name')
    # surname = request.args.get('surname')
    # network_name = request.args.get('network_name')
    # phone_number = request.args.get('phone_number')
    # print(state, name, surname, network_name, phone_number)

    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        request.method + ' ' + request.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        #request.body,
    ))

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
    response = json.loads(response.content.decode('utf-8'))
    print("response['access_token']:", response['access_token'])
    print("response['expires_in']:", response['expires_in'])
    print("response['refresh_token']:", response['refresh_token'])
    print("response['token_type']:", response['token_type'])

    return response


#
# curl -v -X POST 'https://oauth.yandex.ru/token' \
# -H 'Content-type: application/x-www-form-urlencoded' \
# -H 'Authorization: Basic MGM1NDZjZmFhNGU4NDBjNGI0MWJjYTRhOGFmMmU1NmE6Y2UxMGIxZjU0MTQxNGJhOWEwYmYzMTM5ZDBkZjlmNDk=' \
# -d 'grant_type=authorization_code&code=6678635'
def get_user(ya_token):
    url = 'https://login.yandex.ru/info?'
    params = {
        'format': 'json',
        'jwt_secret': 'secret_try'
    }
    headers = {
        'Authorization': 'OAuth ' + ya_token,
    }

    response = requests.get(url, params=params, headers=headers)
    print('STATUS_CODE: ', response.status_code)
    print('content: ', response.content)
    print("url:", url)
    print("params:", params)
    response = json.loads(response.content.decode('utf-8'))
    return response

#
# curl -v GET 'https://login.yandex.ru/info?' \
# -H 'Authorization: OAuth y0_AgAAAAAetcd8AAk1CgAAAADemu3gczbsmIFPTsuSiWY_l8Q0_STY3h8' \
# -d 'format=json&jwt_secret=secret_try'
