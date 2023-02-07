from enum import Enum
import json

from flask import Flask, request

app = Flask(__name__)
data = []


class Type(int, Enum):
    SelfService = 1  # автомойка самообслуживания
    Contactless = 2  # безконтактная
    Manual = 3  # ручная мойка
    Portal = 4  # портальная
    Tunnel = 6  # тунельная
    Dry = 5  # сухая


class BoxStatus(int, Enum):
    Free = 1  # – свободен
    Busy = 2  # - занят
    Unavailable = 3  # – недоступен(закрыт на ремонте)


class CostType(int, Enum):
    Fix = 1  # – фиксированная
    PerMinute = 2  # – стоимость


class Carwash:
    def __init__(self, id, enable, name, address, Location,
                 Type, stepCost, limitMinCost, Boxes, Price):
        self.id = id
        self.enable = enable
        self.name = name
        self.address = address
        self.location = Location  # перевести в список из lon и lat?
        self.type = Type  # Enum('type', ['SelfService', 'Contactless',
        # 'Manual', 'Portal', 'Tunnel', 'Dry'])
        self.stepCost = stepCost
        self.limitMinCost = limitMinCost
        self.boxes = Boxes
        self.price = Price

    """def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
"""


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
    # id, enable, name, address, Location, Type, stepCost,
    # limitMinCost, Boxes, Price):
    SmartCarWash = Carwash(
        '1', True, 'Smart Car',
        'Moscow, Simferopolskiy 19',
        [55.651110, 37.606092],
        Type.SelfService,
        200.0,
        1000.0,
        # Boxes
        [
            ['1', BoxStatus.Free],
            ['2', BoxStatus.Busy],
            ['3', BoxStatus.Unavailable],
            ['4', BoxStatus.Free],
        ],
        # Price
        [
            ['1', 'Description1', 1000.0, CostType.Fix],
            ['2', 'Description2', 2000.0, CostType.Fix],
            ['3', 'Description3', 3000.0, CostType.Fix],
            ['4', 'Description4', 4000.0, CostType.Fix],
        ],
    )
    SmartWashCAR = Carwash(
        1, True, 'Smart Car',
        'Moscow, Simferopolskiy 19',
        [55.651110, 37.606092],
        Type.SelfService,
        200.0,
        1000.0,
        # Boxes
        [
            ['1', BoxStatus.Busy],
            ['2', BoxStatus.Free],
            ['3', BoxStatus.Free],
            ['4', BoxStatus.Unavailable],
        ],
        # Price
        [
            ['1', 'Description1', 4000.0, CostType.PerMinute],
            ['2', 'Description2', 3000.0, CostType.PerMinute],
            ['3', 'Description3', 2000.0, CostType.PerMinute],
            ['4', 'Description4', 1000.0, CostType.PerMinute],
        ],
    )

    data.append(SmartCarWash)
    data.append(SmartWashCAR)
    return json.dumps([obj.__dict__ for obj in data])


if __name__ == '__main__':
    # run app in debug mode on port 5000
    API_KEY = '123456'

    app.run(port=5000)

################################################################
