from flask import Flask, request, Response, abort

import carwash_list
import carwash_order
import ping_carwash_box

app = Flask(__name__)

API_KEY = ['123456', '7tllmnubn49ghu5qrep97']

########################################################################

@app.route('/carwash/ping')
def return_carwash_ping():
    apiKey = request.args.get('apikey')
    print('try_apiKey: ' + apiKey)

    if apiKey in API_KEY:
        status = ping_carwash_box.main(request)
        response = Response(status=status, mimetype="application/json")

    else:
        result = 'Error, Something is wrong...'
        status = 401

        response = Response(result, status=status, mimetype="application/json")
    print(response)
    return response

@app.route('/carwash/list')
def return_carwash_list():
    try_apiKey = request.args.get('apikey')
    print('try_apiKey: ' + try_apiKey)
    if try_apiKey in API_KEY:
        result = carwash_list.main(request)
        status = 200
    else:
        result = 'Error, Something is wrong...'
        status = 401
    response = Response(result, status=status, mimetype="application/json")
    return response


@app.route('/carwash/order', methods=['POST'])
def make_carwash_order():
    result = carwash_order.main(request)
    return result


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080)
