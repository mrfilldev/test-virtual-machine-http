import json
import uuid
from types import SimpleNamespace

from bson import json_util
from flask import render_template, url_for, redirect, jsonify

from ..db import database
from ..db.models import Boxes, BoxStatus, PricesCarWash, Point, Types, Carwash, CategoryAuto


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
                for obj in range(len(prices_list)):
                    if prices_list[obj]._id == j.split('_')[1]:
                        obj = obj
                        print(obj)
                        categories = prices_list[obj].categoryPrice
                        print(categories)
                        for category in categories:
                            if category.category == j.split('_')[2]:
                                sum_default = category.sum
                                prices.append(PricesCarWash(j.split('_')[1], j.split('_')[2], sum_default))
                                break
                        break
    return prices


def show_list_price():
    all_prices = database.col_prices.find({})
    prices_list = []
    count_prices = 0
    for count_prices, i in enumerate(list(all_prices)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print(price_obj)
        prices_list.append(price_obj)
    print(prices_list)
    context = {
        'prices_list': prices_list,
        'count_prices': count_prices,
    }
    return context


def list_carwashes(g):
    if 'networks' in g.user_db:
        network = g.user_db['networks'][0]
        all_carwashes = database.col_carwashes.find({'network_id': network})
        print('network:', network)
        network = database.col_networks.find({'_id': network})
        data = json.loads(json_util.dumps(network))
        data = json.dumps(data, default=lambda x: x.__dict__)
        network_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))[0]  # SimpleNamespace
        print('network_obj:', network_obj)
    else:
        all_carwashes = database.col_carwashes.find({})
        network_obj = None
    carwashes_list = []
    count_carwashes = 0

    for count_carwashes, i in enumerate(list(all_carwashes)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        carwashes_list.append(carwash_obj)
        print(carwash_obj, '\n')

    enum_type_list = list(Types)
    print('enum_type_list: ', enum_type_list)

    context = {
        'carwashes_list': carwashes_list,
        'count_carwashes': count_carwashes,
        'network_obj': network_obj,
        'enum_type_list': enum_type_list,
        'TYPES': Types
    }
    return render_template('view_carwash/carwash_list.html', context=context)


def create_carwash_obj(request, g):
    if request.method == 'POST':
        print('\n################################################################\n')
        dict_of_form = request.form.to_dict(flat=False)
        print(dict_of_form)
        print('################################################################\n')

        for k, v in dict_of_form.items():
            print(k, '-> ', v)

        print('\n################################################################\n')

        id = uuid.uuid4().hex
        name_carwash = request.form['name']
        address_carwash = request.form['address']
        location_carwash = Point(request.form['lat'], request.form['lon'])
        types = Types.SelfService.name
        stepCost = 10.0
        limitMinCost = 100.0
        boxes = create_boxes(int(request.form['amount_boxes']))
        enable: bool = True if request.form['status'] == 'enable' else False
        status = enable
        login_administrator = request.form['login_administrator']
        prices = create_prices(request, dict_of_form)

        print(prices)

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
        new_carwash_dict['network_id'] = g.user_db['networks'][0]

        # network = g.user_db['networks'][0]
        # print('network:', network)
        # network = database.col_networks.find({'_id': network})
        # data = json.loads(json_util.dumps(network))
        # data = json.dumps(data, default=lambda x: x.__dict__)
        # network_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))[0]  # SimpleNamespace
        # print('network_obj:', network_obj)
        #
        # print('network_obj.carwashes:', print(network_obj.carwashes))
        # print(list(network_obj.carwashes).append(new_carwash_dict['_id']))
        # set_fields = {'$set': {
        #     'carwashes': [],
        # }}
        # database.col_networks.update_one({'_id': g.user_db['networks'][0]}, set_fields)

        database.col_carwashes.insert_one(new_carwash_dict)
        database.col_carwashes_admins.insert_one(
            {
                '_id': new_carwash_dict['_id'],
                'login': login_administrator,
                'access_level': 'carwash_admin',
            }
        )
        return redirect(url_for('carwash_blueprint.carwashes_list'))
    all_prices = database.col_prices.find({})
    prices_list = []
    count_prices = 0
    for count_prices, i in enumerate(list(all_prices)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print(price_obj)
        prices_list.append(price_obj)
    print(prices_list)

    context = {
        'create_new': True,
        'carwash': None,
        'prices_list': prices_list,
        'count_prices': count_prices,
    }
    return render_template("view_carwash/carwash_detail.html", context=context)


def pin_admin(carwash_id, login):
    user = database.col_users.find_one({'email': login})  # dict
    print(user)
    data = json.loads(json_util.dumps(user))
    data = json.dumps(data, default=lambda x: x.__dict__)
    user_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    if user_obj is None:
        pass
    else:
        user = {'_id': user_obj._id}
        print('user-admin._id: ', user)
        set_fields = {'$set': {
            'PinnedCarwashId': carwash_id,
        }}
        database.col_users.update_one(user, set_fields)


def get_carwash_obj(carwash_id):
    carwash_obj = database.col_carwashes.find_one({'_id': carwash_id})  # dict
    data = json.loads(json_util.dumps(carwash_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    return carwash_obj


def update_cost_of_price(dict_of_form, carwash_id):
    carwash_obj = get_carwash_obj(carwash_id)
    print('Price: ', carwash_obj.Price)
    print('Price._id: ', carwash_obj.Price._id)
    print('Price.categoryPrice: ', carwash_obj.Price.categoryPrice)

    print('carwash_obj.Price.categoryPrice.Compact: ', carwash_obj.Price.categoryPrice.Compact)
    # for key in dict_of_form.keys():
    #     if 'price' in key:
    #         id = key.split('_')[1]
    #         # print(id)
    #         cat = key.split('_')[2]
    #         # print(cat)
    #         for price in carwash_obj.Price:
    #             for category in price.categoryPrice:
    #                 # print('category: ', category)
    #                 category.sum = (dict_of_form[key])[0]
    #                 # print('category.sum: ', category.sum)


def update_carwash_obj(request, carwash_id):
    form = request.form
    print('\n################################################################\n')
    dict_of_form = request.form.to_dict(flat=False)
    print(dict_of_form)
    print('################################################################\n')

    for k, v in dict_of_form.items():
        print(k, '-> ', v)

    print('\n################################################################\n')

    dict_of_form = request.form.to_dict(flat=False)
    new_boxes_json = json.dumps(create_boxes(int(form['amount_boxes'])), default=lambda x: x.__dict__)
    new_boxes_list_of_dict = json.loads(new_boxes_json)  # , object_hook=lambda d: SimpleNamespace(**d))
    if 'status' not in form:
        enable: bool = False
    else:
        enable: bool = True

    update_cost_of_price(dict_of_form, carwash_id)

    old_carwash = {'_id': carwash_id}
    print('old_carwash: ', old_carwash)
    set_fields = {'$set': {
        'Enable': enable,
        'Name': form['name'],
        'Address': form['address'],
        'Location': {'lat': form['lat'], 'lon': form['lon']},
        'Type': Types.SelfService.name,
        'Boxes': new_boxes_list_of_dict,
        # 'Price': ,
        'CarwashAdmin': form['login_administrator'],
    }}
    new_carwash = database.col_carwashes.update_one(old_carwash, set_fields)
    pin_admin(carwash_id, form['login_administrator'])
    print('UPDATE FIELDS: ', set_fields)
    print('UPDATE DATA: ', new_carwash)


def back_carwash_detail(g, request, carwash_id):
    if request.method == 'POST':
        update_carwash_obj(request, carwash_id)
        return redirect(url_for('carwash_blueprint.carwashes_list'))
    print(type(carwash_id))
    carwash_obj = database.col_carwashes.find_one({'_id': carwash_id})  # dict
    print(carwash_obj)
    data = json.loads(json_util.dumps(carwash_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print('carwash_obj: ', carwash_obj)
    amount_boxes = len(carwash_obj.Boxes)

    all_prices = database.col_prices.find()
    prices_list = []
    count_prices = 0
    for count_prices, i in enumerate(list(all_prices)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        prices_list.append(price_obj)
        print(price_obj)

    enum_list = list(CategoryAuto)
    print(enum_list)
    print('carwash_obj ', carwash_obj)
    context = {
        'carwash': carwash_obj,
        'amount_boxes': amount_boxes,
        'prices_list': prices_list,
        'count_prices': count_prices,
        'enum_list': enum_list
    }
    return render_template("view_carwash/carwash_detail.html", context=context)


def check_price_status(request, carwash_id):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print(data, carwash_id)
    print('\n################################################################\n')
    arr_of_id_price = []
    for i in data.keys():
        arr_of_id_price.append(i)
    price_objects = database.col_prices.find({'_id': {'$in': arr_of_id_price}})
    prices_list = []
    for i in price_objects:
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        prices_list.append(price_obj)
    print(prices_list)

    carwash = {'_id': carwash_id}
    print('carwash: ', carwash)
    set_fields = {'$set': {
        'Price': json.loads(json.dumps(prices_list, default=lambda x: x.__dict__)),
    }}
    database.col_carwashes.update_one(carwash, set_fields)
    # обработка данных
    # формирование ответа
    response = {'status': 'success'}
    return jsonify(response)


def carwash_delete(carwash_id):
    database.col_carwashes.delete_one({'_id': carwash_id})
    print('deleted carwash_id:', carwash_id)
    return redirect(url_for('carwash_blueprint.carwashes_list'))
