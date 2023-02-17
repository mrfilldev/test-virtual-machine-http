import asyncio
import enum
import json
import os
import time
from types import SimpleNamespace

import boto3
import requests
from datetime import datetime as dt

from urllib.parse import quote_plus as quote

import pymongo
from dotenv import load_dotenv

load_dotenv()

################################################################
# from aws_requests_auth.aws_auth import AWSRequestsAuth
client = boto3.client(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
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

async def get_order_messege_queue():
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
            order = msg.get('Body')
            print('Received message: ', msg.get('Body'))
            print('TYPE: ', type(msg.get('Body')))
            write_into_db(order)
            # get the message
            client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg.get('ReceiptHandle')
            )
            # Delete processed messages
            print('Successfully deleted message by receipt handle "{}"'.format(msg.get('ReceiptHandle')))
            order = json.loads(msg.get('Body'), object_hook=lambda d: SimpleNamespace(**d))
            await send_accept_status(order)

        break  # ЗАЧЕМ BREAK?!


def write_into_db(order: str):
    order = json.loads(order, object_hook=lambda d: SimpleNamespace(**d))
    # order = eval(order)
    url = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
        user=quote('user1'),
        pw=quote('mrfilldev040202'),
        hosts=','.join([
            'rc1a-f0wss58juko3mx2p.mdb.yandexcloud.net:27018'
        ]),
        rs='rs01',
        auth_src='db1')
    dbs = pymongo.MongoClient(
        url,
        tlsCAFile='/home/mrfilldev/.mongodb/root.crt')['db1']

    print('Writing into DB')

    # dbs - название бд
    # test_items - название чего?
    # mycol - название коллекции
    if order.Status == 'OrderCreated':
        order = dbs.tst_items.mycol.insert_one({
            "_id": order.Id,
            "DateTime": order.DateTime,
            "BoxNumber": order.BoxNumber,
            "CarWashId": order.CarWashId,
            "ContractId": order.ContractId,
            "Status": order.Status,
            "Sum": order.Sum,
            "SumCompleted": order.SumCompleted,
            "SumPaidStationCompleted": order.SumPaidStationCompleted,
            # :order.Services, # не удалять: наличие этого параметра зависит от того, какой тип заказа; при fix -
            # отсутствует

        })
        print('WRITED ORDER: ', order)
        print('ORDER_ID:', order.inserted_id)

        print("Объекты в БД МОНГО:", dbs.list_collection_names(), '\n')
        print('Объекты в коллекции', dbs.tst_items.find())
