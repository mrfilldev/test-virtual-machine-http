import json
import os
import time

import boto3
from flask import Flask, request, Response

from flask_app import carwash_list, carwash_order
import ping_carwash_box
from flask_app.carwash_order import Status

app = Flask(__name__)

API_KEY = ['123456', '7tllmnubn49ghu5qrep97']
queue_orders = 'https://message-queue.api.cloud.yandex.net/b1gjm9f9sf1pbis8lhhp/dj600000000bqnoc01b1/test-tanker-carwsh-orders'
client = boto3.client(
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    service_name='sqs',
    endpoint_url='https://message-queue.api.cloud.yandex.net',
    region_name='ru-central1'
)
queue_url = client.create_queue(QueueName='test-tanker-carwsh-orders').get('QueueUrl')


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
async def make_carwash_order():
    order = carwash_order.main(request)
    status = 400 if order is None else 200
    response = Response(status=status)

    # SQS запись
    if (status == 200) & (order.Status == Status.OrderCreated.name):

        carwash_order.send_order_sqs(json.dumps(order, default=lambda x: x.__dict__))

    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
