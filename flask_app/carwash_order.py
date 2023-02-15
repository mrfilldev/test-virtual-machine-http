import enum
import json
import os
from types import SimpleNamespace

import boto3

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


class Status(enum.IntEnum):
    nNone = 0
    OrderCreated = 1
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

        self.Status = Status[str(status)]
        self.Sum = sum
        self.SumCompleted = sum_completed
        self.SumPaidStationCompleted = sum_paid_station_completed

    def display_info(self):
        details = f"""
# Новый Заказ: #
            Id: {self.Id} 
            DateTime: {self.DateTime}  
            BoxNumber: {self.BoxNumber}
            CarWashId: {self.CarWashId} 
            ContractId: {self.ContractId} 
            Status: {self.Status} 
            Sum: {self.Sum}
            SumCompleted: {self.SumCompleted} 
            SumPaidStationCompleted: {self.SumPaidStationCompleted}
# Конец заказа #\n"""
        print(details)


def make_order(request):
    data = json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d))

    if data.Status != Status.UserCanceled.name or Status.CarWashCanceled.name:
        #  Создание объекта класса Order
        new_order = Order(
            data.Id,
            data.DateCreate,
            data.CarWashId,
            data.BoxNumber,
            data.Status,
            data.Sum,
            data.SumCompleted,
            # data.Services, # не удалять: наличие этого параметра зависит от того, какой тип заказа; при fix - отсутствует
            data.ContractId,
            data.SumPaidStationCompleted
        )
        new_order.display_info()

    return data


def send_order_sqs(order):
    print(
        'Sending order:...',
        client.send_message(
            QueueUrl=queue_url,
            MessageBody=order
        )
    )


def check_the_status(request):
    data = json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d))
    result = data.Status
    print("result:", result)
    print("Status: ", data.Status)
    return result


def main(request):
    status = check_the_status(request)
    if status == Status.OrderCreated.name:
        print("REQUEST: ", request)
        print("REQUEST.DATA: ", request.data)
        return make_order(request)
    elif status == Status.UserCanceled.name:
        print("REQUEST: ", request)
        print("REQUEST.DATA: ", request.data)
        print("Order canceled...")
        return None
    else:
        print("REQUEST: ", request)
        print("REQUEST.DATA: ", request.data)
        return None
