import enum
import json

from flask import Flask, request

app = Flask(__name__)
data = []

address_my = 'Симферопольский бульвар, 19к1, Москва, 117452'  # 55.650378, 37.606487
address_crystal = '1-й Красногвардейский проезд, 19, Москва, 123112'  # 55.750843, 37.536693
address_carwash_my = 'Ялтинская улица, 1, Москва, 117452'  # 55.650383, 37.611447


########################################################################

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


class Prices:
    def __init__(self, id, description, cost, costType):
        self.Id = id
        self.description = description
        self.cost = cost
        self.costType = costType


class Point:  # enum.Enum):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


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

def test_collect_objs_in_list():
    location_my = Point(55.650378, 37.606487)
    location_my_dict = {'longitude': '55.650378', 'latitude': '37.606487'}

    box1 = Boxes('1', BoxStatus.Free)
    box2 = Boxes('2', BoxStatus.Unavailable)
    box3 = Boxes('1', BoxStatus.Free)
    box4 = Boxes('2', BoxStatus.Busy)

    group_of_boxes1 = [box1, box2]
    group_of_boxes2 = [box3, box4]

    price1 = Prices('1', 'Description1', 1000.0, CostType.Fix.name)
    price2 = Prices('2', 'Description2', 2000.0, CostType.Fix.name)
    price3 = Prices('3', 'Description3', 3000.0, CostType.Fix.name)
    price4 = Prices('4', 'Description4', 4000.0, CostType.Fix.name)

    price_group1 = [price1, price2]
    price_group2 = [price3, price4]

    print(location_my)

    my_home = Carwash(
        '1', True, 'Мой дом :)',
        address_my,

        location_my,
        Type.FullService.name,
        200.0,
        1000.0,
        # Boxes
        group_of_boxes1,

        price_group1,

    )
    crystal_carwash = Carwash(
        '1', True, 'Crystal city',
        address_crystal,

        location_my,
        Type.FullService.name,
        200.0,
        1000.0,
        # Boxes
        group_of_boxes2,

        price_group2,

    )

    data.append(my_home)
    data.append(crystal_carwash)

    return json.dumps(data, default=lambda x: x.__dict__)


if __name__ == '__main__':
    API_KEY = '123456'

    app.run(host='0.0.0.0')

################################################################
# return simplejson.dumps(data)#[obj.__dict__ for obj in data])
# return simplejson.dumps(data, default=default)
# location_crystal.toJson(),
# location_my.toJson(),
# location_my.dict_back(),
# print('location_my: ' + location_my.__annotations__)
# location_crystal = Point(55.750843, 37.536693)
# location_carwash_my = Point(55.650383, 37.611447)
# [
#     ['1', BoxStatus.Free.name],
#     ['2', BoxStatus.Busy.name],
#     ['3', BoxStatus.Unavailable.name],
#     ['4', BoxStatus.Free.name],
# ],
# Price
# [
#     ['1', 'Description1', 1000.0, CostType.Fix.name],
#     ['2', 'Description2', 2000.0, CostType.Fix.name],
#     ['3', 'Description3', 3000.0, CostType.Fix.name],
#     ['4', 'Description4', 4000.0, CostType.Fix.name],
# ],
#
#
# [
#         #     ['1', BoxStatus.Busy.name],
#         #     ['2', BoxStatus.Free.name],
#         #     ['3', BoxStatus.Free.name],
#         #     ['4', BoxStatus.Unavailable.name],
#         # ],
#         # Price
# [
#         #     ['1', 'Description1', 4000.0, CostType.PerMinute.name],
#         #     ['2', 'Description2', 3000.0, CostType.PerMinute.name],
#         #     ['3', 'Description3', 2000.0, CostType.PerMinute.name],
#         #     ['4', 'Description4', 1000.0, CostType.PerMinute.name],
#         # ],


# def to_json(self):
#     return self.__str__()

# def dict_back(self):
#     return {"latitude": str(self.latitude), "longitude": str(self.longitude)}
# def forJson(self):
#     return self.longitude, self.latitude
#
# def toJson(self):
#     return json.dumps(self, default=lambda o: o.__dict__)

# def default(obj):
#     if hasattr(obj, 'to_json'):
#         return obj.to_json()
#     raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

# def to_json(self):
#     return self.__str__()

# def dict_back(self):
#     return {"number": str(self.number), "status": str(self.status)}
# def to_json(self):
#     return self.__str__()

# def dict_back(self):
#     return {
#         "Id": str(self.Id), "Description": str(self.description),
#         "Cost": str(self.cost), "CostType": str(self.costType)
#     }
