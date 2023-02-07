import enum
import json

from flask import Flask, request

app = Flask(__name__)
data = []


class Type(enum.IntEnum):
    SelfService = 1   # автомойка самообслуживания
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
            ['1', BoxStatus.Free.name],
            ['2', BoxStatus.Busy.name],
            ['3', BoxStatus.Unavailable.name],
            ['4', BoxStatus.Free.name],
        ],
        # Price
        [
            ['1', 'Description1', 1000.0, CostType.Fix.name],
            ['2', 'Description2', 2000.0, CostType.Fix.name],
            ['3', 'Description3', 3000.0, CostType.Fix.name],
            ['4', 'Description4', 4000.0, CostType.Fix.name],
        ],
    )
    SmartWashCAR = Carwash(
        '1', True, 'Smart Car',
        'Moscow, Simferopolskiy 19',
        [55.651110, 37.606092],
        Type.SelfService,
        200.0,
        1000.0,
        # Boxes
        [
            ['1', BoxStatus.Busy.name],
            ['2', BoxStatus.Free.name],
            ['3', BoxStatus.Free.name],
            ['4', BoxStatus.Unavailable.name],
        ],
        # Price
        [
            ['1', 'Description1', 4000.0, CostType.PerMinute.name],
            ['2', 'Description2', 3000.0, CostType.PerMinute.name],
            ['3', 'Description3', 2000.0, CostType.PerMinute.name],
            ['4', 'Description4', 1000.0, CostType.PerMinute.name],
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
