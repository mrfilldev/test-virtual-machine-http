import json
from types import SimpleNamespace

from bson import json_util

from ..db import database
from ..db.models import Boxes, BoxStatus, PricesCarWash, Point, Types, Carwash


def create_boxes(amount_boxes: int):
    group_of_boxes = []
    for i in range(1, amount_boxes + 1):
        group_of_boxes.append(Boxes(i, BoxStatus.Free.name))

    result = group_of_boxes
    print('result', result)
    return result


def create_prices(request, dict_of_form):
    prices = []

    all_prices = database.col_prices.find({})
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

    id = database.col_carwashes.count_documents({}) + 1
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
        stepCost, limitMinCost, boxes, prices, login_administrator
    )
    new_carwash_json = json.dumps(new_carwash, default=lambda x: x.__dict__)
    print('TYPE: ', type(new_carwash_json))
    print('data: ', new_carwash_json)
    new_carwash_dict = json.loads(new_carwash_json)  # , object_hook=lambda d: SimpleNamespace(**d))
    print('TYPE: ', type(new_carwash_dict))
    print('data: ', new_carwash_dict)
    new_carwash_dict['_id'] = new_carwash_dict.pop('Id')

    database.col_carwashes.insert_one(new_carwash_dict)
    database.col_carwashes_admins.insert_one(
        {
            '_id': new_carwash_dict['_id'],
            'login': login_administrator,
            'access_level': 'carwash_admin',
        }
    )


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
    new_carwash = database.col_carwashes.update_one(old_carwash, set_fields)
    print('UPDATE FIELDS: ', set_fields)
    print('UPDATE DATA: ', new_carwash)
    return new_carwash
