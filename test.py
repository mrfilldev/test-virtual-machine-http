import enum
import json

import simplejson
from flask import Flask, request

app = Flask(__name__)
data = []

address_my = 'Симферопольский бульвар, 19к1, Москва, 117452'  # 55.650378, 37.606487
address_crystal = '1-й Красногвардейский проезд, 19, Москва, 123112'  # 55.750843, 37.536693
address_carwash_my = 'Ялтинская улица, 1, Москва, 117452'  # 55.650383, 37.611447


def default(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


class Type(enum.IntEnum):
    FullService = 7
    SelfService = 1  # автомойка самообслуживания
    Contactless = 2  # безконтактная
    Manual = 3  # ручная мойка
    Portal = 4  # портальная
    Tunnel = 5  # тунельная
    Dry = 6  # сухая


class BoxStatus(enum.IntEnum):
    Free = 1  # – свободен
    Busy = 2  # - занят
    Unavailable = 3  # – недоступен(закрыт на ремонте)


class CostType(enum.IntEnum):
    Fix = 1  # – фиксированная
    PerMinute = 2  # – стоимость


class Boxes:
    def __init__(self, numbers, boxStatus):
        self.number = numbers
        self.status = boxStatus

    def to_json(self):
        return self.__str__()


class Prices:
    pass


class Point:  # enum.Enum):

    def __init__(self, latitude, longitude):
        self.latitude = latitude,
        self.longitude = longitude,

    def dict_back(self):
        return {"latitude": self.latitude, "longitude": self.longitude}
    # def forJson(self):
    #     return self.longitude, self.latitude
    #
    # def toJson(self):
    #     return json.dumps(self, default=lambda o: o.__dict__)


class Carwash:
    def __init__(self, id, enable, name, address, Location,
                 Type, stepCost, limitMinCost, Boxes, Price):
        self.Id = id
        self.Enable = enable
        self.Name = name
        self.Address = address
        self.Location = Location  # перевести в список из lon и lat?
        self.Type = Type  # Enum('type', ['SelfService', 'Contactless',
        # 'Manual', 'Portal', 'Tunnel', 'Dry'])
        self.StepCost = stepCost
        self.LimitMinCost = limitMinCost
        self.Boxes = Boxes
        self.Price = Price


################################################################
"""def my_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)

    # Далее можно описывать и другие свои типы, например MyFooFooBar
    # elif isinstance(obj, MyFooFooBar):
    #     return obj.get_super_foo_bar_value()

    # Если не удалось определить тип:
    return str(obj)"""


################################################################

@app.route('/carwash/list')
def example():
    try_apiKey = request.args.get('apikey')
    print('try_apiKey: ' + try_apiKey)
    if try_apiKey == API_KEY:
        result = test_collect_objs_in_list()
    else:
        result = 'Error, Something is wrong...'
    print(result)  # ????????
    return result


################################


location_my = Point(55.650378, 37.606487)
# location_my_dict = {'longitude': '55.650378', 'latitude': '37.606487'}
# print('location_my: ' + location_my.__annotations__)
location_crystal = Point(55.750843, 37.536693)
location_carwash_my = Point(55.650383, 37.611447)

box1 = Boxes('1', BoxStatus.Free)
box2 = Boxes('2', BoxStatus.Unavailable)
box3 = Boxes('1', BoxStatus.Free)
box4 = Boxes('2', BoxStatus.Busy)

group_of_boxes1 = [box1.to_json(), box2.to_json()]
group_of_boxes2 = [box3.to_json(), box4.to_json()]

print(location_my)

my_home = Carwash(
    '1', True, 'Мой дом :)',
    address_my,
    # location_my.toJson(),
    location_my.dict_back(),
    Type.FullService,
    200.0,
    1000.0,
    # Boxes
    group_of_boxes1,
    # [
    #     ['1', BoxStatus.Free.name],
    #     ['2', BoxStatus.Busy.name],
    #     ['3', BoxStatus.Unavailable.name],
    #     ['4', BoxStatus.Free.name],
    # ],
    # Price
    [
        ['1', 'Description1', 1000.0, CostType.Fix.name],
        ['2', 'Description2', 2000.0, CostType.Fix.name],
        ['3', 'Description3', 3000.0, CostType.Fix.name],
        ['4', 'Description4', 4000.0, CostType.Fix.name],
    ],
)


for i in my_home:
    print(i)
