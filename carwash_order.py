import enum
import json
import urllib.request
import time
import asyncio
from datetime import datetime as dt
from types import SimpleNamespace
from flask import Response
import requests

URL_DEV = 'http://app.tst.tanker.yandex.net'
API_KEY = '7tllmnubn49ghu5qrep97'


class Status(enum.IntEnum):
    nNone = 0
    OrderCreated = 1  # "OrderCreated"
    Expire = 2
    Completed = 3
    CarWashCanceled = 4
    UserCanceled = 5


class Services:

    def __init__(self, id: str, description: str, cost: float):
        self.id = id
        self.description = description
        self.cost = cost


class Order:
    def __init__(self, id: str, date_create_date_time: str, car_wash_id,
                 box_number: str, status, sum: float, sum_completed: float,
                 # services,
                 contract_id: str, sum_paid_station_completed: float):
        self.Id = id
        self.DateTime = date_create_date_time
        self.BoxNumber = box_number
        self.CarWashId = car_wash_id
        self.ContractId = contract_id
        # self.Services = Services(services[0].Id, services[0].Description, services[0].Cost)

        self.Status = Status[str(status)]
        self.Sum = sum
        self.SumCompleted = sum_completed
        self.SumPaidStationCompleted = sum_paid_station_completed

    def display_info(self):
        print(
            "# Новый Заказ: #\n"
            f"Id: {self.Id} DateTime: {self.DateTime}  BoxNumber: {self.BoxNumber}\n"
            f"CarWashId: {self.CarWashId} ContractId: {self.ContractId} Status: {self.Status} Sum: {self.Sum}\n"
            f"SumCompleted: {self.SumCompleted} SumPaidStationCompleted: {self.SumPaidStationCompleted}\n"
            "# Конец заказа #\n"
        )


def make_order(request):
    data = json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d))
    # data = json.loads(request.data, object_hook=lambda d: custom_decoder(**d))

    if data.Status != 'UserCanceled' or 'СarWashCanceled':
        #  Создание объекта класса Order
        new_order = Order(
            data.Id, data.DateCreate, data.CarWashId,
            data.BoxNumber, data.Status, data.Sum, data.SumCompleted,

            # не удалять: наличие этого параметра зависит от того, какой тип заказа; при fix - отсутствует
            # data.Services,

            data.ContractId, data.SumPaidStationCompleted
        )
        print(new_order.display_info())
    return data
    # task1 = asyncio.create_task(send_accept_status(data.Id, data.Sum))
    # print('Task done?')


def send_200_OK_status():
    status = 200
    response = Response(status=status, mimetype="application/json")
    return response


async def send_accept_status(data):
    url = URL_DEV + "/api/carwash/order/accept/"
    params = {
        'apikey': API_KEY,
        'orderId': data.Id
    }
    requests.get(url, params=params)

    # data = {
    #     "apikey": API_KEY,
    #     "orderId": data.Id,
    # }
    #
    # headers = {'content-type': 'application/json'}
    # requests.post(url, data=data, headers=headers)
    print("url:", url)
    print("params:", params)
    # print('data: ', data)

    await asyncio.sleep(5)
    #  response = urllib.request.urlopen(url)
    # data = response.read()
    # dict = json.loads(data)
    # print('dict: ', dict)
    # task2 = asyncio.create_task(send_completed_status(id, sum))


def send_canceled_status(id):
    reason = 'Тестовая отмена'
    url = URL_DEV + "/api/carwash/order/canceled"
    data = {
        "apikey": API_KEY,
        "orderId": id,
        "reason": reason,

    }

    headers = {'content-type': 'application/json'}
    requests.post(url, data=data, headers=headers)

    print("url:", url)

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    print('data: ', data)
    print('dict: ', dict)


async def send_completed_status(data):
    extended_date = dt.now().strftime("%d-%m-%Y %H:%M%S")
    print('extended_date: ', extended_date)
    extended_order_id = 'test_id' + str(extended_date)
    print('extended_order_id: ', extended_order_id)

    url = URL_DEV + "/api/carwash/order/accept/"
    params = {
        'apikey': API_KEY,
        'orderId': data.Id,
        'sum': data.Sum,
        'extendedOrderId': extended_order_id,
        'extended_date': extended_date

    }
    requests.get(url, params=params)

    # url = URL_DEV + "/api/carwash/order/completed"
    # data = {
    #     "apikey": API_KEY,
    #     "orderId": data.Id,
    #     "sum": data.Sum,
    #     "extendedOrderId": extended_order_id,
    #     "extendedDate": extended_date
    # }
    # headers = {'content-type': 'application/json'}
    # requests.post(url, data=data, headers=headers)
    print("url:", url)
    print('params: ', params)
    # print('data: ', data)
    await asyncio.sleep(8)
    # response = urllib.request.urlopen(url)
    # data = response.read()
    # dict = json.loads(data)
    # print('dict: ', dict)


def check_the_status(request):
    data = json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d))
    if data.Status == 'OrderCreated':
        result = True
    else:
        result = False
    print("result:", result)
    print("Status: ", data.Status)
    return result


async def main(request):
    if check_the_status(request):
        print("REQUEST: ", request)
        print("REQUEST.DATA: ", request.data)
        data = make_order(request)
        task1 = asyncio.create_task(send_accept_status(data))
        task2 = asyncio.create_task(send_completed_status(data))
    else:
        print("REQUEST: ", request)
        print("REQUEST.DATA: ", request.data)

    data_back = json.loads(request.data)
    return data_back

################################################################
# print(json.loads(request.data, default=lambda x: x.__dict__))

# new_order = Order(data.I
# d)
# print(type(new_order.Status.name))
# print(new_order.Status.name)
# print(type(new_order.Status.value))
# print(data)
