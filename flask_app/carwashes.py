import enum
import json
from types import SimpleNamespace

from config.config import Config


class Types(enum.IntEnum):
    SelfServiceFixPrice = 1  # автомойка самообслуживания Fix Price
    SelfService = 2  # автомойка самообслуживания
    Contactless = 3  # безконтактная
    Manual = 4  # ручная мойка
    Portal = 5  # портальная
    Tunnel = 6  # тунельная
    Dry = 7  # сухая


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


class Prices:
    def __init__(self, id, description, cost, costType):
        self.Id = id
        self.description = description
        self.cost = cost
        self.costType = costType


class Point:  # enum.Enum):
    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.lon = longitude

    def return_list(self):
        list_obj = [self.lat, self.lon]
        return list_obj


class Carwash:
    def __init__(self, id, enable, name, address, Location: Point,
                 Type, stepCost, limitMinCost, Boxes, Price):
        self.Id = id
        self.Enable = enable
        self.Name = name
        self.Address = address
        self.Location = Location
        self.Type = Type
        self.StepCost = stepCost
        self.LimitMinCost = limitMinCost
        self.Boxes = Boxes
        self.Price = Price


def create_boxes(amount_boxes: int):
    group_of_boxes = []
    for i in range(amount_boxes):
        group_of_boxes.append(Boxes(i, BoxStatus.Free.name))

    result = group_of_boxes
    print('result', result)


def create_carwash_obj(request):
    for i in request.form:
        print(i, request.form[i])

    name_carwash = request.form['name']
    address_carwash = request.form['address']
    location_carwash = Point(request.form['lat'], request.form['lon'])
    types = Types.SelfServiceFixPrice.name
    stepCost = 10.0
    limitMinCost = 100.0
    boxes = create_boxes(request.form['boxes'])


def smthn_old():
    location_my = Point(55.650378, 37.606487)
    location_crystal = Point(55.750654, 37.536016)
    # location_my_dict = {'longitude': '55.650378', 'latitude': '37.606487'}

    box1 = Boxes('1', BoxStatus.Free.name)
    box2 = Boxes('1', BoxStatus.Free.name)
    box3 = Boxes('2', BoxStatus.Free.name)
    box4 = Boxes('2', BoxStatus.Free.name)
    box5 = Boxes('3', BoxStatus.Free.name)
    box6 = Boxes('3', BoxStatus.Free.name)
    box7 = Boxes('4', BoxStatus.Busy.name)
    box8 = Boxes('4', BoxStatus.Busy.name)

    group_of_boxes1 = [box1, box3, box5, box7]
    group_of_boxes2 = [box2, box4, box6, box8]

    price1 = Prices('1', 'Кузов', 1000.0, CostType.Fix.name)
    price2 = Prices('2', 'Кузов + коврики', 1700.0, CostType.Fix.name)
    price3 = Prices('3', 'Комплекс', 2200.0, CostType.Fix.name)
    price4 = Prices('4', 'Комплекс + антидождь', 2500.0, CostType.Fix.name)
    price5 = Prices('5', 'Комплекс + чернение', 2500.0, CostType.Fix.name)
    price6 = Prices('6', 'Комплекс ALL IN', 3500.0, CostType.Fix.name)

    price_group1 = [price1, price3, price5]
    price_group2 = [price2, price4, price6]

    # res = Config.col_carwashes.aggregate([{'$count': 'total'}])
    # print("Config.col_carwashes.aggregate([{'$count': 'total'}]) ",res)
    # res = Config.col_carwashes.count_documents({})
    # print("Config.col_carwashes.count_documents({}) ",res)
    # res = Config.col_carwashes.estimated_document_count()
    # print(res)
    # res = Config.col_carwashes.find().count()
    # print(res)
    id = Config.col_carwashes.count_documents({}) + 1
    enable = True
    name = form.Name.data
    print("name: ", name)
    print("type_name: ", )
    address = form.Address.data
    print("address: ", address)

    location = Point(str(form.Location.data).split(', ')[0], str(form.Location.data).split(', ')[1])
    print("location: ", location)
    print("type_name: ", )

    types = Types.SelfServiceFixPrice.name
    stepCost = 200.0
    limitMinCost = 1000.0
    boxes = group_of_boxes1
    price = price_group1

    new_carwash = Carwash(
        id, enable, name, address, location, types,
        stepCost, limitMinCost, boxes, price
    )
    new_carwash_json = json.dumps(new_carwash, default=lambda x: x.__dict__)
    print('TYPE: ', type(new_carwash_json))
    print('data: ', new_carwash_json)
    new_carwash_dict = json.loads(new_carwash_json)  # , object_hook=lambda d: SimpleNamespace(**d))
    print('TYPE: ', type(new_carwash_dict))
    print('data: ', new_carwash_dict)
    res = Config.col_carwashes.insert_one(new_carwash_dict)
    print('WRITED CARWASH: ', res)
