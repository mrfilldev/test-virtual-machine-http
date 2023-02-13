import enum
import json
from types import SimpleNamespace
from flask import jsonify
from urls import app


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

    # Вывод данных
    print("REQUEST: " + str(request))
    print("REQUEST.DATA: " + str(request.data))


def check_the_status(request):
    data = json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d))
    if data.Status == 'UserCanceled' or 'СarWashCanceled' or 'Expire':
        result = False
    else:
        result = True
    print("Status: ", data.Status)
    return result


def main(request):
    if check_the_status(request):
        print("REQUEST: ", request)
        print("REQUEST.DATA: ", request.data)
        make_order(request)

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
