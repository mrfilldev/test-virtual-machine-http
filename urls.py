from flask import Flask, request

import carwash_list
import carwash_order

app = Flask(__name__)


########################################################################

@app.route('/carwash/list')
def return_carwash_list():
    return carwash_list.main(request)


@app.route('/carwash/order', methods=['POST'])
def make_carwash_order():
    result = carwash_order.main(request)
    return result


if __name__ == '__main__':
    API_KEY = '123456'

    app.run(host='127.0.0.1', port=8080)
