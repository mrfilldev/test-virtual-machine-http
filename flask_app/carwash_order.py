import enum
import json
import os
from types import SimpleNamespace


from urls import client, queue_url


class Status(enum.IntEnum):
    nNone = 0
    OrderCreated = 1
    Expire = 2
    Completed = 3
    CarWashCanceled = 4 # ?!
    UserCanceled = 5
    StationCanceled = 6


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

        #[BsonId]
        self.Id = id
        self._id = id
        self.DateCreate = date_create_date_time
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
            DateTime: {self.DateCreate}  
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

    if data.Status == Status.OrderCreated:
        #  Создание объекта класса Order
        new_order = Order(
            data.Id,
            data.DateCreate,
            data.CarWashId,
            data.BoxNumber,
            data.Status,
            data.Sum,
            data.SumCompleted,
            # data.Services, # не удалять: наличие этого параметра зависит от того, какой тип заказа; при fix -
            # отсутствует
            data.ContractId,
            data.SumPaidStationCompleted
        )
        new_order.display_info()

    elif data.Status == Status.StationCanceled.name:
        new_order = Order(
            data.Id,
            data.DateCreate,
            data.CarWashId,
            data.BoxNumber,
            data.Status,
            data.Sum,
            0.0,  # data.SumCompleted,
            # data.Services, # не удалять: наличие этого параметра зависит от того, какой тип заказа; при fix -
            # отсутствует
            data.ContractId,
            0.0  # data.SumPaidStationCompleted
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

    order = make_order(request)

    if order.Status == Status.OrderCreated.name:
        print("REQUEST: ", request)
        print("REQUEST.DATA: ", request.data)

        send_order_sqs(json.dumps(order, default=lambda x: x.__dict__))

    elif order.Status == Status.UserCanceled.name:
        print("REQUEST: ", request)
        print("REQUEST.DATA: ", request.data)
        print("Order canceled...")

    elif order.Status == Status.StationCanceled.name:
        print("REQUEST: ", request)
        print("REQUEST.DATA: ", request.data)
        print("Order canceled...")

    else:
        print("REQUEST: ", request)
        print("REQUEST.DATA: ", request.data)

