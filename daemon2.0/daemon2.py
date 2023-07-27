import asyncio
import json

import time
import traceback
from datetime import datetime as dt
from types import SimpleNamespace

from bson import json_util
from dateutil.parser import parse

from web_params.params import Py_mongo_db, Sqs_params
# from ..configuration.config import Config

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

    url = URL_DEV + "/api/carwash/order/completed"
    params = {
        'apikey': API_KEY,
        'orderId': order['_id'],
        'sum': order['Sum'],
        'extendedOrderId': order['_id'],
        'extended_date': dt.now().isoformat(timespec='microseconds'),
    }
    requests.get(url, params=params)

    print("url:", url)
    print('params: ', params)


async def send_canceled_status(order, reason):
    print('REASON: ', reason)
    print("START SEND CANCEL STATUS")

    url = URL_DEV + "/api/carwash/order/canceled"
    params = {
        'apikey': API_KEY,
        'orderId': order['_id'],
        'reason': reason
    }
    requests.get(url, params=params)
    print("url:", url)
    print("params:", params)


async def make_mongo_id(order):
    order['_id'] = order.pop('Id')
    current_carwash = Py_mongo_db.col_carwashes.find_one({'_id': order['CarWashId']})
    data = json.loads(json_util.dumps(current_carwash))
    data = json.dumps(data, default=lambda x: x.__dict__)
    current_carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    order['network_id'] = current_carwash_obj.network_id
    print(order.keys())
    print(order.values())
    return order


async def auto_compliting_order_in_box_4(order):
    data = json.loads(json_util.dumps(order))
    data = json.dumps(data, default=lambda x: x.__dict__)
    order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    print('order_obj:', order_obj)


async def write_into_db(order):
    print('Writing into DB')
    print('order:', order)

    print("'order['DateCreate']: '", order['DateCreate'], type(order['DateCreate']))
    print("'order['DateCreate']: '", parse(order['DateCreate']), type(parse(order['DateCreate'])))

    # res = Py_mongo_db.col_orders.insert_one(order)
    # print('WRITED ORDER: ', res)
    # print('ORDER_ID:', res.inserted_id)
    # print('Объекты в коллекции', Py_mongo_db.col_orders.find())
    # await auto_compliting_order_in_box_4(order)


async def update_order(order):
    old_order = {'_id': order['_id']}
    set_command = {"$set": {
        "Status": order['Status'],
    }}
    upd_order = Py_mongo_db.col_orders.update_one(old_order, set_command)
    print('updated order: ', upd_order)


async def update_order_status(order, status):
    old_order = {'_id': order['_id']}
    set_command = {"$set": {
        "Status": status,
    }}
    upd_order = Py_mongo_db.col_orders.update_one(old_order, set_command)
    print('updated order: ', upd_order)
    await  set_busy_status_box(order)


async def update_order_canceled(order, status):
    old_order = {'_id': order['_id']}
    set_command = {"$set": {
        "Status": status,
        "DateEnd": order['DateEnd'],
        "Reason": order['Reason'],
    }}

    upd_order = Py_mongo_db.col_orders.update_one(old_order, set_command)
    print('updated order: ', upd_order)


def get_carwash_obj(carwash_id):
    carwash_obj = Py_mongo_db.col_carwashes.find_one({'_id': carwash_id})  # dict
    data = json.loads(json_util.dumps(carwash_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print('carwash_obj: ', carwash_obj)
    return carwash_obj


async def set_busy_status_box(order):
    carwash_id = order['CarWashId']
    box_number = order['BoxNumber']

    carwash_obj = get_carwash_obj(carwash_id)
    print('carwash_obj.Boxes.box_number', carwash_obj.Boxes)
    for i in carwash_obj.Boxes:
        if i.number == box_number:
            i.status = 'Busy'

    carwash = {'_id': carwash_id}
    set_command = {"$set": {
        "Boxes": carwash_obj.Boxes,
    }}
    print(set_command)
    # upd_order = Py_mongo_db.col_carwashes.update_one(carwash, set_command)
    # print('updated order: ', upd_order)


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
                        match message["new_status"]:
                            case 'Accepted':
                                print('Accepted')
                                if eval(message["order"])["ContractId"] == "OWN":
                                    await update_order_status(eval(message['order']), 'Accepted')
                                else:
                                    await send_accept_status(eval(message["order"]))
                                    await update_order_status(eval(message['order']), 'Accepted')
                                print('Accepted')
                            case 'Completed':
                                if eval(message["order"])["ContractId"] == "OWN":
                                    await update_order_status(eval(message['order']), 'Completed')
                                else:
                                    await send_completed_status(eval(message["order"]))
                                    await update_order_status(eval(message['order']), 'Completed')
                                print('Completed')
                            case 'Canceled':
                                if eval(message["order"])["ContractId"] == "OWN":
                                    await update_order_status(eval(message["order"]), 'StationCanceled')
                                else:
                                    await send_canceled_status(eval(message["order"]), reason='StationCanceled')
                                    await update_order_status(eval(message["order"]), 'StationCanceled')
                                print('Canceled')
                    case "createOrder":
                        print('CreateOrder')
                        order = await make_mongo_id(eval(message['order']))
                        print(f'order: {type(order)} \n', order)
                        await write_into_db(order)

                    case "cancelOrder":
                        print('CancelOrder')
                        order = await make_mongo_id(eval(message['order']))
                        print(f'order: {type(order)} \n', order)
                        await update_order(order)
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
                print(f'EXEPTION: \n{type(Exception)}: e', error)  # добавить логгер
