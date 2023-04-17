import enum
import json
import sys
from types import SimpleNamespace

sys.path.append('..')
from ..configuration.config import Sqs_params

client = Sqs_params.client
queue_url = Sqs_params.queue_url


def to_camel_case(request):
    print('###to_camel_case')
    dictionary1 = json.loads(request.data.decode('utf-8'))  # bytes object -> dict
    dictionary2 = {}
    for key in dictionary1:
        dictionary2[key[0].upper() + key[1:]] = dictionary1[key]
    print(dictionary2.keys())
    data = json.dumps(dictionary2, default=lambda x: x.__dict__)  # dict -> json
    print('data: ', type(data), data, '\n')
    data = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # json -> simplenamespace
    print('to_camel_case###')
    return data


class Status(enum.IntEnum):
    nNone = 0
    OrderCreated = 1
    Expire = 2
    Completed = 3
    CarWashCanceled = 4
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
                 contract_id: str, sum_paid_station_completed: float):
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


class OrderCanceled:
    def __init__(self, CarWashId, BoxNumber,
                 Id, ContractId, Sum, Status,
                 DateCreate, DateEnd,
                 Reason):
        self.Id = Id
        self.CarWashId = CarWashId
        self.BoxNumber = BoxNumber
        self.ContractId = ContractId
        self.Sum = Sum
        self.Status = Status
        self.DateCreate = DateCreate
        self.DateEnd = DateEnd
        self.Reason = Reason

    def display_info(self):
        details = f"""
# Отмена Заказа: #
            Id: {self.Id} 
            CarWashId: {self.CarWashId} 
            BoxNumber: {self.BoxNumber}
            ContractId: {self.ContractId} 
            Sum: {self.Sum}
            Status: {self.Status} 
            DateCreate: {self.DateCreate}  
            DateEnd: {self.DateEnd}  
# Конец #\n"""
        print(details)


def make_order(data):
    print('DATA:       ', data)
    match data.Status:
        case Status.OrderCreated.name:
            # Создание объекта класса Order
            # data.Services, не удалять: наличие этого параметра зависит от того,
            # какой тип заказа; при fix -# отсутствует
            new_order = Order(
                data.Id, data.DateCreate, data.CarWashId, data.BoxNumber, data.Status, data.Sum,
                data.SumCompleted, data.ContractId, data.SumPaidStationCompleted
            )
            new_order.display_info()
        case _:
            new_order = OrderCanceled(
                data.CarWashId,
                data.BoxNumber,
                data.Id,
                data.ContractId,
                data.Sum,
                data.Status,
                data.DateCreate,
                data.DateEnd,
                data.Reason
            )
            new_order.display_info()
    return data


def send_new_order_sqs(order):
    dict_to_sqs = {}
    dict_to_sqs['order'] = order
    dict_to_sqs['task'] = 'createOrder'
    print(
        'Sending order:...',
        client.send_message(
            QueueUrl=queue_url,
            MessageBody=dict_to_sqs
        )
    )


def send_cancel_order_sqs(order):
    dict_to_sqs = {}
    dict_to_sqs['order'] = order
    dict_to_sqs['task'] = 'cancelOrder'
    print(
        'Sending order:...',
        client.send_message(
            QueueUrl=queue_url,
            MessageBody=dict_to_sqs
        )
    )


def check_the_status(request):
    data = json.loads(request.data, object_hook=lambda d: SimpleNamespace(**d))
    result = data.Status
    print("result:", result)
    print("Status: ", data.Status)
    return result


def main(request):
    print("REQUEST: ", request)
    print("REQUEST.DATA: ", request.data)
    data = to_camel_case(request)
    order = make_order(data)

    match order.Status:
        case Status.OrderCreated.name:
            send_new_order_sqs(json.dumps(order, default=lambda x: x.__dict__))
        case Status.UserCanceled.name:
            print("SQS <- Status.UserCanceled")
            # update_order(order)
            send_cancel_order_sqs(json.dumps(order, default=lambda x: x.__dict__))
        case _:
            pass

# def check_enable():
#     pass
#
#
# def update_order(data):
#     old_order = {'_id': data.Id}
#     set_command = {"$set": {"Status": "UserCanceled"}}
#     new_order = database.col_orders.update_one(old_order, set_command)
#     print('UPDATE DATA: ', new_order)
#     # Response(status=200)
