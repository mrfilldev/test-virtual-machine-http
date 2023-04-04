import enum
import json
from types import SimpleNamespace

from configuration.config import Config
from configuration.config import Sqs_params



def to_camel_case(request):
    dictionary1 = json.loads(request.data.decode('utf-8'))  # bytes object -> dict
    dictionary2 = {}
    # dictionary1 = json.loads(string.decode('utf-8'))  # bytes object -> dict
    dictionary2 = {}
    for key in dictionary1:
        # dictionary[key[0].upper() + key[1:]] = dictionary.pop(key)
        dictionary2[key[0].upper() + key[1:]] = dictionary1[key]

    print(dictionary2.keys())
    data = json.dumps(dictionary2, default=lambda x: x.__dict__) # dict -> json
    print('data: ', type(data), data, '\n')
    data = json.loads(data, object_hook=lambda d: SimpleNamespace(**d)) # json -> simplenamespace
    return data

    ########################################################################
    # последняя версия
    # print('request.data: ', type(request.data), request.data)
    # data = json.loads(request.data.decode('utf-8'))  # bytes object -> dict
    # #data = json.loads(request.decode('utf-8'))  # bytes object -> dict
    # print('data: ', type(data), data, '\n')
    # # data = str(data)
    # print('data: ', type(data), data, '\n')
    # print('Magic?')
    # # data = re.sub(r'_(\w)', lambda x: x.group(1).title(), data)
    # data = {k.title(): v for k, v in data.items()}
    #
    # print('data: ', type(data), data, '\n')
    # # data = eval(data)
    # print('data: ', type(data), data, '\n')
    # data = json.dumps(data, default=lambda x: x.__dict__)
    # print('data: ', type(data), data, '\n')
    # data = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    # print('data: ', type(data), data, '\n')
    # return data
    ########################################################################

    # """print('request.data: ', type(request.data), request.data)
    # data = json.loads(request.data.decode('utf-8'))  # bytes object -> dict
    # print('data: ', type(data), data, '\n')
    # data = str(data)
    # print('data: ', type(data), data, '\n')
    # data = re.sub(r'_(\w)', lambda x: x.group(1).upper(), data)
    # print('data: ', type(data), data, '\n')
    # data = eval(data)
    # print('data: ', type(data), data, '\n')
    # data = json.dumps(data, default=lambda x: x.__dict__)
    # print('data: ', type(data), data, '\n')
    # data = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    # print('data: ', type(data), data, '\n')
    # return data"""
    #
    # for k, v in data.items():
    #     k = k[0].title() + k[1:]
    #     result = {k: v}
    #     print(result)
    #
    # result = json.dumps(result, default=lambda x: x.__dict__)
    # data = json.loads(result, object_hook=lambda d: SimpleNamespace(**d))
    # return data


class Status(enum.IntEnum):
    nNone = 0
    OrderCreated = 1
    Expire = 2
    Completed = 3
    CarWashCanceled = 4  # ?!
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
        # [BsonId]
        self.Id = id
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


def make_order(data):
    print('DATA:       ', data)
    try:
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
    except AttributeError:
        if data.Status == Status.UserCanceled.name:
            update_order(data)
    return data


def send_order_sqs(order):
    print(
        'Sending order:...',
        Sqs_params.client.send_message(
            QueueUrl=Sqs_params.queue_url,
            MessageBody=order
        )
    )
    #return Response(status=200)


def check_the_status(request):
    data = json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d))
    result = data.Status
    print("result:", result)
    print("Status: ", data.Status)
    return result


def check_enable():
    pass


def update_order(data):
    old_order = {'Id': data.Id}
    set_command = {"$set": {"Status": "UserCanceled"}}
    new_order = Config.col_orders.update_one(old_order, set_command)
    print('UPDATE DATA: ', new_order)
    #Response(status=200)


def main(request):
    print("REQUEST: ", request)
    print("REQUEST.DATA: ", request.data)
    data = to_camel_case(request)
    order = make_order(data)

    if order.Status == Status.OrderCreated.name:
        send_order_sqs(json.dumps(order, default=lambda x: x.__dict__))

    elif order.Status == Status.UserCanceled.name:
        print("Order canceling by user...")
        update_order(order)

    elif order.Status == Status.StationCanceled.name:
        print("Order canceled...")

    else:
        pass
