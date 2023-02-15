import asyncio
import os
import time

import boto3
import requests
from datetime import datetime as dt

################################################################
# from aws_requests_auth.aws_auth import AWSRequestsAuth
client = boto3.client(
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    service_name='sqs',
    endpoint_url='https://message-queue.api.cloud.yandex.net',
    region_name='ru-central1'
)
queue_orders = 'https://message-queue.api.cloud.yandex.net/b1gjm9f9sf1pbis8lhhp/dj600000000bqnoc01b1/test-tanker-carwsh-orders'
queue_url = client.create_queue(QueueName='test-tanker-carwsh-orders').get('QueueUrl')
################################################################
URL_DEV = 'http://app.tst.tanker.yandex.net'
API_KEY = '7tllmnubn49ghu5qrep97'


async def send_accept_status(order):
    print("Start SEND ACCEPT STATUS")
    await asyncio.sleep(5)
    print("Start SEND ACCEPT STATUS")
    url = URL_DEV + "/api/carwash/order/accept"
    params = {
        'apikey': API_KEY,
        'orderId': order.Id
    }

    x = requests.get(url, params=params)
    print('STATUS_CODE: ', x.status_code)
    print("url:", url)
    print("params:", params)
    await asyncio.sleep(1)
    await send_completed_status(order)


async def send_canceled_status(data):
    reason = 'Тестовая отмена'
    url = URL_DEV + "/api/carwash/order/canceled"
    params = {
        'apikey': API_KEY,
        'orderId': data.Id,
        'reason': reason
    }
    requests.get(url, params=params)
    print("url:", url)
    print("params:", params)


async def send_completed_status(order):
    print("Start SEND COMPLETED STATUS")

    extended_date = dt.now().strftime("%d-%m-%Y %H:%M%S")
    print('extended_date: ', extended_date)
    extended_order_id = 'test_id' + str(extended_date)
    print('extended_order_id: ', extended_order_id)

    url = URL_DEV + "/api/carwash/order/completed"
    params = {
        'apikey': API_KEY,
        'orderId': order.Id,
        'sum': order.Sum,
        'extendedOrderId': extended_order_id,
        'extended_date': extended_date

    }
    requests.get(url, params=params)

    print("url:", url)
    print('params: ', params)


# task = asyncio.create_task(carwash_order.send_accept_status(order))

def get_order_messege_queue():
    while True:

        messages = client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            VisibilityTimeout=60,
            WaitTimeSeconds=20
        ).get('Messages')

        print('MESSAGES', messages)

        if messages is None:
            print('Сообщение не обнаружено')
            print("ОЖИДАНИЕ 0.5")
            time.sleep(0.5)
            continue

        for msg in messages:
            print('Received message: ', msg.get('Body'))
            # get the message
            client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg.get('ReceiptHandle')
            )
            # Delete processed messages
            print('Successfully deleted message by receipt handle "{}"'.format(msg.get('ReceiptHandle')))

        break


def write_into_db(order):
    print('Writing into DB')
    pass