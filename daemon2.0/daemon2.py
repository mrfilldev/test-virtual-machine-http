import asyncio
import json

import time
import traceback
from datetime import datetime as dt
from random import randint
from types import SimpleNamespace

from web_params.params import Py_mongo_db, Sqs_params

import requests

from dotenv import load_dotenv

load_dotenv()

db_carwashes = Py_mongo_db.col_carwashes

URL_DEV = 'http://app.tst.tanker.yandex.net'
API_KEY = '7tllmnubn49ghu5qrep97'

dict_reason = {
    'Completed': 'Выполнено успешно',
    'CarWashCanceled': 'Отмена заказа Мойкой',
    'UserCanceled': 'Отмена заказа пользователем',
    'StationCanceled': 'Отмена заказа Системой Станций Моек',
    'SystemAggregator_Error': 'Отмена заказа Системой Агрегации',
}


async def send_accept_status(order):
    print("Start SEND ACCEPT STATUS")
    url = URL_DEV + "/api/carwash/order/accept"
    params = {
        'apikey': API_KEY,
        'orderId': order['_id']
    }
    x = requests.get(url, params=params)
    print('STATUS_CODE: ', x.status_code)
    print("url:", url)
    print("params:", params)
    await asyncio.sleep(1)


async def send_completed_status(order):
    print("Start SEND COMPLETED STATUS")

    await update_order_status(order, 'Completed')

    extended_date = dt.now().strftime("%d-%m-%Y %H:%M%S")
    print('extended_date: ', extended_date)
    extended_order_id = 'test_id' + str(extended_date)
    print('extended_order_id: ', extended_order_id)

    url = URL_DEV + "/api/carwash/order/completed"
    params = {
        'apikey': API_KEY,
        'orderId': order['_id'],
        'sum': order['Sum'],
        'extendedOrderId': extended_order_id,
        'extended_date': extended_date

    }
    requests.get(url, params=params)

    print("url:", url)
    print('params: ', params)


async def send_canceled_status(order, reason):
    print('REASON: ', reason)
    print("START SEND CANCEL STATUS")
    rand_time = randint(1, 20)

    await update_order_status(order, reason)

    print("SEND CANCEL in ", rand_time)
    await asyncio.sleep(rand_time)

    url = URL_DEV + "/api/carwash/order/canceled"
    params = {
        'apikey': API_KEY,
        'orderId': order['_id'],
        'reason': dict_reason[reason]
    }
    requests.get(url, params=params)
    print("url:", url)
    print("params:", params)


async def make_mongo_id(order):
    order['_id'] = order.pop('Id')
    print(order.keys())
    print(order.values())
    # await write_into_db(order)
    return order


async def write_into_db(order):
    print('Writing into DB')
    res = Py_mongo_db.col_orders.insert_one(order)

    print('WRITED ORDER: ', res)
    print('ORDER_ID:', res.inserted_id)
    print('Объекты в коллекции', Py_mongo_db.col_orders.find())


async def update_order_status(order, status):
    set_command = {"$set": {"Status": status}}
    old_order = {'_id': order['_id']}
    print('_id: ', order['_id'])

    print('UPDATE STATUS: ', status)
    new_order = Py_mongo_db.col_orders.update_one(old_order, set_command)
    print('UPDATE DATA: ', new_order)
    # Response(status=200)


async def main_func():
    while True:
        messages = Sqs_params.client.receive_message(
            QueueUrl=Sqs_params.queue_url,
            MaxNumberOfMessages=10,
            VisibilityTimeout=60,
            WaitTimeSeconds=20
        ).get('Messages')
        print(f'MESSAGES: {messages}\n')
        if messages is None:
            print('Сообщение не обнаружено')
            print("ОЖИДАНИЕ 0.5")
            time.sleep(0.5)
            continue

        for msg in messages:
            # order = msg.get('Body')
            print('Received message: ', msg.get('Body'))
            print('TYPE: ', type(msg.get('Body')))
            message = eval(msg.get('Body'))
            print('message: ', message)
            print('TYPE: ', type(message))
            try:
                # проверка на тип сообщения:
                # changeStatus - изменение статуса
                # createOrder - создание заказа
                match message["task"]:
                    case "changeStatus":
                        print('changeStatus')
                        match message["body"]["changeStatus"]:
                            case 'Accept':
                                print('Accept')
                                # await send_accept_status(message["body"])
                            case 'Completed':
                                print('Completed')
                                # await send_completed_status(message["body"])
                            case 'CarWashCanceled':
                                print('CarWashCanceled')
                                # await send_carWashCanceled_status(message["body"])
                            case 'UserCanceled':
                                print('UserCanceled')
                                # await send_userCanceled_status(message["body"])
                    case "createOrder":
                        print('CreateOrder')
                        #  await make_some_noize(order)
                        order = await make_mongo_id(eval(message['order']))
                        print(order)
                        #await write_into_db(order)


                    case "cancelOrder":
                        print('CancelOrder')
                        print(message['order'])
                        #  await make_some_noize(order)
                        pass
                    case _:
                        raise ValueError("Неопознанное сообщение: " + message)

                # Delete processed messages
                print('Сообщение удалено: "{}"'.format(msg.get('ReceiptHandle')))
                Sqs_params.client.delete_message(
                    QueueUrl=Sqs_params.queue_url,
                    ReceiptHandle=msg.get('ReceiptHandle')
                )
            except Exception as error:
                # write to log
                # await send_canceled_status(order, reason='SystemAggregator_Error')
                traceback.print_exc()
                print(f'EXEPTION: \n{type(Exception)}: e', Exception)  # добавить логгер
