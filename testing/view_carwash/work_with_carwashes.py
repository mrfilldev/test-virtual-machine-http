import json
import uuid
from types import SimpleNamespace

from bson import json_util
from flask import render_template, url_for, redirect, jsonify, abort

from ..db import database
from ..db.models import Boxes, BoxStatus, PricesCarWash, Point, Types, Carwash, CategoryAuto, Prices


def create_boxes(amount_boxes: int):
    group_of_boxes = []
    for i in range(1, amount_boxes + 1):
        group_of_boxes.append(Boxes(i, BoxStatus.Free.name))

    result = group_of_boxes
    print('result', result)
    return result


def create_prices(request, dict_of_form, update=False, carwash_id=None):
    prices = []
    prices_list = []
    count_prices = 0

    if not update:
        all_prices = database.col_prices.find({})
        for count_prices, i in enumerate(list(all_prices)[::-1], 1):
            data = json.loads(json_util.dumps(i))
            data = json.dumps(data, default=lambda x: x.__dict__)
            price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

            print(price_obj)
            delattr(price_obj, 'costType')
            delattr(price_obj, 'name')
            delattr(price_obj, 'description')
            print(price_obj)

            prices_list.append(price_obj)
        print('prices_list:\n', prices_list)
        for j in dict_of_form:
            if 'price' in j:
                print(j.split('_'))
                if request.form[j] != '':
                    prices.append(PricesCarWash(id=j.split('_')[1], category=j.split('_')[2], sum=request.form[j]))
                elif request.form[j] == '':
                    for i in all_prices:
                        data = json.loads(json_util.dumps(i))
                        data = json.dumps(data, default=lambda x: x.__dict__)
                        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
                        print(price_obj)
                        if price_obj._id == j.split('_')[1]:
                            for price in price_obj.categoryPrice:
                                if price.category == j.split('_')[2]:
                                    sum_default = price.sum
                                    prices.append(
                                        PricesCarWash(id=j.split('_')[1], category=j.split('_')[2], sum=sum_default)
                                    )
        result_arr = []
        for price_obj in prices_list:
            for price in prices:
                if price_obj._id == price._id:
                    for obj_of_existing_price in price_obj.categoryPrice:
                        if obj_of_existing_price.category == price.category:
                            obj_of_existing_price.sum = price.sum
            setattr(price_obj, "status", 'turn_off')
            result_arr.append(price_obj)
        return result_arr
    else:
        print('...update in process...\n')
        print('carwash_id:\n', carwash_id)
        carwash_obj = get_carwash_obj(carwash_id)
        print('carwash_obj:\n', carwash_obj)

        for j in dict_of_form:
            if 'price' in j:
                print(j.split('_'))
                if request.form[j] != '':
                    prices.append(PricesCarWash(id=j.split('_')[1], category=j.split('_')[2], sum=request.form[j]))
                elif request.form[j] == '':
                    for price_obj in carwash_obj.Price:
                        print(price_obj)
                        if price_obj._id == j.split('_')[1]:
                            for price in price_obj.categoryPrice:
                                if price.category == j.split('_')[2]:
                                    sum_default = price.sum
                                    prices.append(
                                        PricesCarWash(id=j.split('_')[1], category=j.split('_')[2], sum=sum_default)
                                    )
        for i in prices:
            print('price: ', vars(i).items())
        result_arr = []
        for price_obj in carwash_obj.Price:
            print('true1')
            for price in prices:
                print('true2')
                if price_obj._id == price._id:
                    print('true3')
                    for obj_of_existing_price in price_obj.categoryPrice:
                        print('true4')
                        if obj_of_existing_price.category == price.category:
                            print('true5')
                            obj_of_existing_price.sum = price.sum
            print('true6')
            # setattr(price_obj, "status", carwash_obj.Price.status)
            result_arr.append(price_obj)
        return result_arr


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


def get_all_prices():
    all_prices = database.col_prices.find({})
    prices_list = []
    for i in all_prices:
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        prices_list.append(price_obj)
    return prices_list


def list_carwashes(g):
    if g.user_db['role'] != 'admin':
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
        'sets_of_prices': get_sets(),
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
        enable = True if 'status' in request.form else False
        #  enable: bool = True if request.form['status'] == 'enable' else False
        status = enable
        login_administrator = request.form['login_administrator']
        prices = request.form['set_of_price']  # create_prices(request, dict_of_form)
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
        new_carwash_dict['network_id'] = g.user_db['networks'][0]

        print(new_carwash_dict)
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


def update_cost_of_price(dict_of_form, carwash_id):
    # prices_67e40c84b5f4455ea17226a6704724cd_Compact ->  ['']
    # prices_67e40c84b5f4455ea17226a6704724cd_MiddleSize ->  ['']
    # prices_67e40c84b5f4455ea17226a6704724cd_Crossover ->  ['']
    # prices_67e40c84b5f4455ea17226a6704724cd_OffRoad ->  ['']
    # prices_67e40c84b5f4455ea17226a6704724cd_MicroBus ->  ['']
    # prices_8c29975f4eca44b8a723ece13a47b548_Compact ->  ['']
    # prices_8c29975f4eca44b8a723ece13a47b548_MiddleSize ->  ['']
    # prices_8c29975f4eca44b8a723ece13a47b548_Crossover ->  ['']
    # prices_8c29975f4eca44b8a723ece13a47b548_OffRoad ->  ['']
    # prices_8c29975f4eca44b8a723ece13a47b548_MicroBus ->  ['']
    arr_of_accepted_prices = {}
    for key in dict_of_form.keys():
        if 'price' in key:
            arr_of_accepted_prices[key] = dict_of_form[key]
    print('Accepted prices: ', arr_of_accepted_prices)

    # carwash_obj = get_carwash_obj(carwash_id)
    # for price in carwash_obj.Price:  # перебор данных существующих в бд
    #     print('price: ', price)
    #     print('price._id: ', price._id)
    #     print('price.categoryPrice: ', price.categoryPrice)
    #     for categoryPrice in price.categoryPrice:
    #         print('price.categoryPrice.category: ', categoryPrice.category)

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
    enable = True if 'status' in form else False

    is_hand_carwash = True if 'is_hand_carwash' in form else False
    is_wheel_station = True if 'is_wheel_station' in form else False
    is_detaling = True if 'is_detaling' in form else False
    print(is_hand_carwash)
    print(is_wheel_station)
    print(is_detaling)

    # update_cost_of_price(dict_of_form, carwash_id)
    # print('UPD_PRICE:', json.loads(json.dumps(create_prices(request, dict_of_form, update=True, carwash_id=carwash_id), default=lambda x: x.__dict__)))

    old_carwash = {'_id': carwash_id}
    print('old_carwash: ', old_carwash)
    set_fields = {'$set': {
        'Enable': enable,
        'Name': form['name'],
        'Address': form['address'],
        'Location': {'lat': form['lat'], 'lon': form['lon']},
        'Type': Types.SelfService.name,
        'Boxes': new_boxes_list_of_dict,
        'Price': request.form['set_of_price'],
        # json.loads(json.dumps(create_prices(request, dict_of_form, update=True, carwash_id=carwash_id),default=lambda x: x.__dict__)),
        'CarwashAdmin': form['login_administrator'],
        'IsCarwash': is_hand_carwash,
        'IsWheelStation': is_wheel_station,
        'IsDetaling': is_detaling,
    }}
    new_carwash = database.col_carwashes.update_one(old_carwash, set_fields)
    pin_admin(carwash_id, form['login_administrator'])
    print('UPDATE FIELDS: ', set_fields)
    print('UPDATE DATA: ', new_carwash)


def get_sets():
    all_sets = database.col_sets_of_prices.find({})
    sets_list = []
    for i in all_sets:
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        set_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        sets_list.append(set_obj)
        print(set_obj, '\n')
    return sets_list


def get_set_of_prices(set_id):
    set_obj = database.col_sets_of_prices.find_one({'_id': set_id})  # dict
    data = json.loads(json_util.dumps(set_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    set_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print(set_obj, '\n')
    return set_obj


def back_carwash_detail(g, request, carwash_id):
    if request.method == 'POST':
        update_carwash_obj(request, carwash_id)
        return redirect(url_for('carwash_blueprint.carwash_detail', carwash_id=carwash_id))
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
        'enum_list': enum_list,
        'set_of_prices': get_set_of_prices(carwash_obj.Price),
        'sets_of_prices': get_sets(),
    }
    return render_template("view_carwash/carwash_detail.html", context=context)


def get_price_obj(price_id):
    price_obj = database.col_prices.find_one({'_id': price_id})  # dict
    data = json.loads(json_util.dumps(price_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    delattr(price_obj, 'costType')
    delattr(price_obj, 'name')
    delattr(price_obj, 'description')
    return price_obj


def get_carwash_obj(carwash_id):
    carwash_obj = database.col_carwashes.find_one({'_id': carwash_id})  # dict
    data = json.loads(json_util.dumps(carwash_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    return carwash_obj


def change_price_status(request, carwash_id):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print(data, carwash_id)
    print('\n################################################################\n')
    arr_of_id_price = []
    carwash_obj = get_carwash_obj(carwash_id)
    print('carwash_obj: ', carwash_obj)
    for price in carwash_obj.Price:
        print('price: ', price)
        if price._id in data.keys():
            price.status = 'active'
        else:
            price.status = 'turn_off'
        arr_of_id_price.append(price._id)

    for price_id in data.keys():
        if price_id not in arr_of_id_price:
            new_price = get_price_obj(price_id)
            new_price.status = 'active'

            carwash_obj.Price.append(new_price)

    print('carwash_obj price: ', carwash_obj.Price)

    carwash = {'_id': carwash_id}
    print('carwash: ', carwash)
    set_fields = {'$set': {
        'Price': json.loads(json.dumps(carwash_obj.Price, default=lambda x: x.__dict__)),
    }}
    print('set_fields: ', set_fields)
    database.col_carwashes.update_one(carwash, set_fields)
    # обработка данных
    # формирование ответа
    response = {'status': 'success'}
    return jsonify(response)


def carwash_delete(carwash_id, g_user_info):
    # database.col_carwashes.delete_one({'_id': carwash_id})
    # print('deleted carwash_id:', carwash_id)
    if g_user_info.user_db['role'] == 'admin' or g_user_info.user_db['role'] == 'network_owner':
        set_fields = {'$set': {
            "hidden", True
        }}
        database.col_carwashes.update_one({'_id': carwash_id}, set_fields)
    return redirect(url_for('carwash_blueprint.carwashes_list'))
