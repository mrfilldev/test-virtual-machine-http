import enum
import json
from types import SimpleNamespace

from bson import json_util

from config.config import Config

db_carwashes = Config.col_carwashes
db_prices = Config.col_prices


class Types(enum.IntEnum):
    SelfServiceFixPrice = 1  # автомойка самообслуживания Fix Price
    SelfService = 2  # автомойка самообслуживания
    Contactless = 3  # безконтактная
    Manual = 4  # ручная мойка
    Portal = 5  # портальная
    Tunnel = 6  # тунельная
    Dry = 7  # сухая


class CategoryAuto(enum.IntEnum):
    Compact = 10
    MiddleSize = 20
    Crossover = 30
    OffRoad = 40
    MicroBus = 50

    def CategoryAutoToDispaly(self, category):
        if category == CategoryAuto.Compact:
            return 'Кат.1'
        elif category == CategoryAuto.MiddleSize:
            return 'Кат.2'
        elif category == CategoryAuto.Crossover:
            return 'Кат.3'
        elif category == CategoryAuto.OffRoad:
            return 'Кат.4'
        elif category == CategoryAuto.MicroBus:
            return 'Кат.5'
        else:
            return category


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


class CostIdSum:
    def __init__(self, category, sum):
        self.category = category
        self.sum = sum


class Prices:
    def __init__(self, id, name, description, cost_id_sum, cost_type):
        self.Id = id
        self.name = name
        self.description = description
        self.categoryPrice = cost_id_sum
        self.costType = cost_type


class PricesCarWash:
    def __init__(self, id, category, cost):
        self.Id = id
        self.categoryPrice = category
        self.cost = cost


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
    for i in range(1, amount_boxes + 1):
        group_of_boxes.append(Boxes(i, BoxStatus.Free.name))

    result = group_of_boxes
    print('result', result)
    return result


def create_prices(request, dict_of_form):
    prices = []

    all_prices = db_prices.find({})
    prices_list = []
    count_prices = 0
    for count_prices, i in enumerate(list(all_prices)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print(price_obj)
        prices_list.append(price_obj)
    print('prices_list:\n', prices_list)

    for j in dict_of_form:
        if 'price' in j:
            print(j.split('_'))
            if request.form[j] != '':
                prices.append(PricesCarWash(j.split('_')[1], j.split('_')[2], request.form[j]))
            elif request.form[j] == '':

                obj = prices_list[int(j.split('_')[1]) - 1]
                print(obj)
                categories = obj.categoryPrice
                print(categories)
                for category in categories:
                    if category.category == j.split('_')[2]:
                        sum_default = category.sum
                        prices.append(PricesCarWash(j.split('_')[1], j.split('_')[2], sum_default))

    return prices


def create_carwash_obj(request):
    print('\n################################################################\n')
    dict_of_form = request.form.to_dict(flat=False)
    print(dict_of_form)
    print('################################################################\n')

    for k, v in dict_of_form.items():
        print(k, '-> ', v)

    print('\n################################################################\n')

    id = Config.col_carwashes.count_documents({}) + 1
    name_carwash = request.form['name']
    address_carwash = request.form['address']
    location_carwash = Point(request.form['lat'], request.form['lon'])
    types = Types.SelfServiceFixPrice.name
    stepCost = 10.0
    limitMinCost = 100.0
    boxes = create_boxes(int(request.form['amount_boxes']))
    enable: bool = True if request.form['status'] == 'enable' else False
    status = enable
    login_administrator = request.form['login_administrator']
    prices = create_prices(request, dict_of_form)

    # prices.append(PricesCarWash(id, i.name, j))
    # print(PricesCarWash(id, i.name, j))
    print(prices)
    # print(dict_of_form['Compact'])
    # print(dict_of_form['MiddleSize'])
    # print(dict_of_form['Crossover'])
    # print(dict_of_form['OffRoad'])
    # print(dict_of_form['MicroBus'])

    new_carwash = Carwash(
        id, status, name_carwash, address_carwash, location_carwash, types,
        stepCost, limitMinCost, boxes, prices
    )
    new_carwash_json = json.dumps(new_carwash, default=lambda x: x.__dict__)
    print('TYPE: ', type(new_carwash_json))
    print('data: ', new_carwash_json)
    new_carwash_dict = json.loads(new_carwash_json)  # , object_hook=lambda d: SimpleNamespace(**d))
    print('TYPE: ', type(new_carwash_dict))
    print('data: ', new_carwash_dict)
    new_carwash_dict['_id'] = new_carwash_dict.pop('Id')
    res = Config.col_carwashes.insert_one(new_carwash_dict)
    print('WRITED CARWASH: ', res)


def update_carwash_obj(request, carwash_id):
    form = request.form
    dict_of_form = request.form.to_dict(flat=False)
    new_boxes_json = json.dumps(create_boxes(int(form['amount_boxes'])), default=lambda x: x.__dict__)
    new_boxes_list_of_dict = json.loads(new_boxes_json)  # , object_hook=lambda d: SimpleNamespace(**d))
    enable: bool = True if form['status'] == 'enable' else False
    new_prices_json = json.dumps(create_prices(request, dict_of_form), default=lambda x: x.__dict__)
    new_prices_list_of_dict = json.loads(new_prices_json)  # , object_hook=lambda d: SimpleNamespace(**d))
    old_carwash = {'_id': int(carwash_id)}
    print('old_carwash: ', old_carwash)
    set_fields = {'$set': {
        'Enable': enable,
        'Name': form['name'],
        'Address': form['address'],
        'Location': {'lat': form['lat'], 'lon': form['lon']},
        'Type': Types.SelfService.name,
        'Boxes': new_boxes_list_of_dict,
        'Price': new_prices_list_of_dict,
    }}
    new_carwash = db_carwashes.update_one(old_carwash, set_fields)
    print('UPDATE FIELDS: ', set_fields)
    print('UPDATE DATA: ', new_carwash)
    return new_carwash


def create_price_obj(request, carwash_id):
    for i in request.form:
        print(i, request.form[i])


def delete_carwash_obj(carwash_id):
    db_carwashes.delete_one({'Id': int(carwash_id)})


def make_price_corrrect_4_tanker(list_price):
    result = []
    for obj_price in list_price:
        price_db_obj = db_prices.find({'Id': int(obj_price['Id'])})
        data = json.loads(json_util.dumps(price_db_obj))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))[0]  # SimpleNamespace
        print('price from db:\n', price_obj)
        print('price already in carwash db:\n', obj_price)
        # Поля которые требуется сформировать
        # Id Name Description Category Cost CostType
        result.append({
            'Id': str(obj_price['Id'] + '_' + obj_price['categoryPrice']),
            'Name': price_obj.name,
            'Description': price_obj.description,
            'Category': obj_price['categoryPrice'],
            'Cost': obj_price['cost'],
            'CostType': price_obj.costType,
        })

    return result


def carwash_list_main():
    all_carwashes = db_carwashes.find({})
    array_of_carwashes = []
    for obj in all_carwashes:
        if '_id' in obj:
            obj.pop('_id')

        print('BEFORE: ', obj['Price'])
        # метод получения всех требуемых данных:
        obj['Price'] = make_price_corrrect_4_tanker(obj['Price'])
        print('AFTER: ', obj['Price'])
        array_of_carwashes.append(obj)

    #     array_of_carwashes.append(obj)
    # print('================================================================')
    # print(array_of_carwashes)
    # print('================================================================')
    result = json.dumps(array_of_carwashes, default=lambda x: x.__dict__)
    # print(result)
    return result
