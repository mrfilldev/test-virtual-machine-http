import asyncio
import json
import os
import time
import traceback
from datetime import datetime as dt
from random import randint
from types import SimpleNamespace

from start_point import dbs
import boto3
import requests
# import pymongo
from dotenv import load_dotenv

# from flask_app.carwash_order import Order
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

dict_reason = {
    'CarWashCanceled': 'Отмена заказа Мойкой',
    'UserCanceled': 'Отмена заказа пользователем',
    'StationCanceled': 'Отмена заказа Станцией Мойки',
}

mycol = dbs.tst_items.mycol



async def send_accept_status(order):
    print("Start SEND ACCEPT STATUS")
    if order.BoxNumber != '3':
        rand_time = randint(1, 20)
        print("SEND ACCEPT in ", rand_time)
        await asyncio.sleep(rand_time)

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


async def send_canceled_status(order, reason):
    print('REASON: ', reason)
    print("START SEND CANCEL STATUS")
    rand_time = randint(1, 20)

    print("SEND CANCEL in ", rand_time)
    await asyncio.sleep(rand_time)

    url = URL_DEV + "/api/carwash/order/canceled"
    params = {
        'apikey': API_KEY,
        'orderId': order.Id,
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

async def user_canceled(order_json):
    after_minute = time.time() + 60
    while time.time() <= after_minute:
        #  проверку в бд
        status_in_db = mycol.find_one()#{'_id': order_json.Id})

        print('Status: ', status_in_db)

        for doc in status_in_db:
            print(doc)

        if status_in_db == 'UserCanceled':
            return True
        await asyncio.sleep(0.1)

    await send_accept_status(order_json)


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
            # order = msg.get('Body')
            print('Received message: ', msg.get('Body'))
            print('TYPE: ', type(msg.get('Body')))
            order_json = json.loads(msg.get('Body'), object_hook=lambda d: SimpleNamespace(**d))
            order = eval(msg.get('Body'))
            print('TYPE: ', type(order))
            try:
                write_into_db(order)

                # get the message
                print('order_json: ', order_json)
                if order_json.BoxNumber == '2':
                    await send_canceled_status(order_json, dict_reason['StationCanceled'])
                elif order_json.BoxNumber == '3':
                    await user_canceled(order_json)
                else:
                    await send_accept_status(order_json)

                # Delete processed messages
                print('Successfully deleted message by receipt handle "{}"'.format(msg.get('ReceiptHandle')))
                client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=msg.get('ReceiptHandle')
                )
            except Exception as error:
                # write to log
                #  message = f'Сбой в работе программы: {error}'
                # logger.exception(message)

                await send_canceled_status(order_json, reason='Ошибка на стороне сервера')
                traceback.print_exc()
                print(f'EXEPTION: \n{type(Exception)}: e', Exception)  # добавить логгер


def write_into_db(order):
    # order = json.loads(order, object_hook=lambda d: SimpleNamespace(**d))

    print('Writing into DB')

    # dbs - название бд
    # test_items - название чего?
    # mycol - название коллекции

    res = dbs.tst_items.mycol.insert_one(order)
    print('WRITED ORDER: ', res)

    print('ORDER_ID:', res.inserted_id)

    print("Объекты в БД МОНГО:", dbs.list_collection_names(), '\n')
    print('Объекты в коллекции', dbs.tst_items.mycol.find())
