import enum
import json
from types import SimpleNamespace

from flask import jsonify


# import requests
class Status(enum.IntEnum):
    nNone = 0
    OrderCreated = 1# "OrderCreated"
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
                 #services,
                 contract_id: str, sum_paid_station_completed: float):
        self.Id = id
        self.DateTime = date_create_date_time
        self.BoxNumber = box_number
        self.CarWashId = car_wash_id
        self.ContractId = contract_id
        #self.Services = Services(services[0].Id, services[0].Description, services[0].Cost)

        self.Status = Status[str(status)]
        self.Sum = sum
        self.SumCompleted = sum_completed
        self.SumPaidStationCompleted = sum_paid_station_completed


def main(request):
    if request.method == 'POST':
        print(request)

        data_back = json.loads(request.data)
        print(request.data)
        data = json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d))
        #data = json.loads(request.data, object_hook=lambda d: custom_decoder(**d))


        # for key in data:
        #     print(key, '->', data[key])

        new_order = Order(
            data.Id, data.DateCreate, data.CarWashId,
            data.BoxNumber, data.Status, data.Sum, data.SumCompleted,
            # data.Services,
            data.ContractId, data.SumPaidStationCompleted
            )
        #new_order = Order(data.I
        # d)
        print("################")

        print("новый объект:")

        print(new_order)
        print(type(new_order.Status.name))
        print(new_order.Status.name)
        print(type(new_order.Status.value))
        print(data)
        return data_back

################################################################
# print(json.loads(request.data, default=lambda x: x.__dict__))
