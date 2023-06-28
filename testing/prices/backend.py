import json
import uuid
import time
from datetime import datetime
from types import SimpleNamespace

from bson import json_util
from flask import render_template, request, jsonify, redirect, url_for

from ..db import database
from ..db.models import CategoryAuto, SetOfPrices, PriceOfSet, CostIdSum, PricesCarWash, priceType

FORMAT = '%Y-%m-%dT%H:%M:%S%Z'



def get_prices_obj_list():
    prices = database.col_prices.find({})
    prices_list = []

    for i in list(prices):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        prices_list.append(price_obj)
    return prices_list


def serializing_sets_collection(all_sets):
    sets_list = []
    for i in all_sets:
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        set_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        sets_list.append(set_obj)
        print(set_obj, '\n')
    return sets_list


def serializing_set(set):
    set_obj = database.col_sets_of_prices.find_one({'_id': set})  # dict
    data = json.loads(json_util.dumps(set_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    set_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print(set_obj, '\n')
    return set_obj


def show_list_sets_prices(g_user_flask):
    if 'networks' in g_user_flask.user_db:
        network = g_user_flask.user_db['networks'][0]
        print('network: ', network)
        all_sets = database.col_sets_of_prices.find({'network': network})
    else:
        all_sets = database.col_sets_of_prices.find({})
    sets_serialized = serializing_sets_collection(all_sets)
    print(sets_serialized)
    context = {
        'prices': get_prices_obj_list(),
        'enum_list': list(CategoryAuto),
        'sets': sets_serialized,
    }
    return render_template('prices/list_sets_price.html', context=context)


def set_create(request, g_user_flask):
    if request.method == 'POST':
        print('\n########################DATA####################################\n')
        data = request.form.to_dict()
        print(data)
        print('\n################################################################\n')

        new_set = SetOfPrices(
            id=uuid.uuid4().hex,
            name=request.form['name'],
            description=request.form['description'],
            prices=[]
        )
        print(new_set)
        new_set = json.loads(json.dumps(new_set, default=lambda x: x.__dict__))
        new_set['network'] = g_user_flask.user_db['networks'][0]
        print(new_set)
        database.col_sets_of_prices.insert_one(new_set)

    response = {'status': 'success'}
    return show_list_sets_prices(g_user_flask)


def find_prices_with_set_id(set_id):
    prices_of_set = []
    prices = database.col_prices.find({'set_id': set_id})  # dict
    for price in prices:
        data = json.loads(json_util.dumps(price))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        prices_of_set.append(price_obj)

    print(prices_of_set)
    return prices_of_set


def update_set_of_prices(request, set_id, g_user_flask):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print(data)
    print('\n################################################################\n')
    set_obj = serializing_set(set_id)
    print('set_obj: ', set_obj)
    print('\n################################################################\n')

    list_prices = find_prices_with_set_id(set_id)
    dict_of_form = request.form.to_dict(flat=False)
    set_prices_id_to_update = set()
    for k, v in dict_of_form.items():
        id = k.split('_')[1]
        category = k.split('_')[2]
        cost = v[0]
        for price in list_prices:
            if price._id == id:
                for categoryPrice in price.categoryPrice:
                    if categoryPrice.category == category:
                        if categoryPrice.sum != cost:
                            print('Need to update')
                            print(id, '->', category, '->', cost)
                            categoryPrice.sum = cost
                            set_prices_id_to_update.add(id)

    print(set_prices_id_to_update)
    for price_id in set_prices_id_to_update:
        for price_obj in list_prices:
            if price_obj._id == price_id:
                print('price_obj: ', price_obj)
                print('price_obj.categoryPrice: ', price_obj.categoryPrice)
                database.col_prices.update_one({'_id': price_obj._id}, {"$set": {
                    "categoryPrice": json.loads(json.dumps(price_obj.categoryPrice, default=lambda x: x.__dict__)),
                    'last_edit': make_last_edit_string(g_user_flask)

                }})


def set_detail(request, set_id, g_user_flask):
    if request.method == 'POST':
        update_set_of_prices(request, set_id, g_user_flask)
    set_obj = serializing_set(set_id)
    set_id_prices = find_prices_with_set_id(set_id)
    context = {
        'set_prices': set_id_prices,
        'set': set_obj,
        'enum_list': list(CategoryAuto),
        'priceType': list(priceType),

    }
    return render_template('prices/set_detail.html', context=context)


def make_last_edit_string(g_user_flask):
    result = time.strftime(FORMAT, time.localtime()) + ' ' + g_user_flask.user_db['_id']
    return result


def create_price(request, set_id, g_user_flask):
    if request.method == 'POST':
        print('\n########################DATA####################################\n')
        data = request.form.to_dict()
        print(data)
        print('set_id: ', set_id)
        print('\n################################################################\n')

        for i in request.form:
            print(i, request.form[i])
        form = request.form
        id = uuid.uuid4().hex
        name = form['name']
        categoryPrice = []
        description = form['description']
        costType = form['costType']
        priceType = form['priceType']

        for i in list(CategoryAuto):
            categoryPrice.append(CostIdSum(i.name, form[str(i.name)]))

        new_price = PriceOfSet(id, set_id, name, description, categoryPrice, costType, priceType)

        print(new_price.categoryPrice)
        print(new_price.set_id)
        for i in new_price.categoryPrice:
            print(f'{i.category} -> {i.sum}')

        # запись в бд
        new_price = eval(json.dumps(new_price, default=lambda x: x.__dict__))
        new_price['last_edit'] = make_last_edit_string(g_user_flask)
        print(new_price)
        print(type(new_price))
        database.col_prices.insert_one(new_price)

    response = {'status': 'success'}
    return jsonify(response)


def update_price(request, price_id, g_user_flask):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print(data)
    print('price: ', price_id)
    print('\n################################################################\n')
    for i in request.form:
        print(i, request.form[i])
    print('1')
    form = request.form
    price_id = {'_id': price_id}
    print('2')
    print('old_carwash: ', price_id)
    categoryPrice = []
    print(list(CategoryAuto))
    for category in list(CategoryAuto):
        print(category)
        print(category.name)
        print(form[str(category.name)])
        categoryPrice.append(CostIdSum(category.name, form[str(category.name)]))
    data = json.dumps(categoryPrice, default=lambda x: x.__dict__)
    categoryPrice = json.loads(data)  # , object_hook=lambda d: SimpleNamespace(**d))
    set_fields = {'$set': {
        'name': form['name'],
        'description': form['description'],
        'categoryPrice': categoryPrice,
        'costType': form['costType'],
        'priceType': form['priceType'],
        'status': 'active',
        'last_edit': make_last_edit_string(g_user_flask)
    }}
    new_price = database.col_prices.update_one(price_id, set_fields)
    print('UPDATE FIELDS: ', set_fields)
    print('UPDATE DATA: ', new_price)


def hide_price(price_id, g_user_flask):
    price_obj = get_price_obj(price_id)
    price_id = {'_id': price_id}
    set_fields = {'$set': {
        'status': 'turn_off',
        'last_edit': make_last_edit_string(g_user_flask),
    }}
    new_price = database.col_prices.update_one(price_id, set_fields)
    print('UPDATE FIELDS: ', set_fields)
    print('UPDATE DATA: ', new_price)
    return redirect(url_for('prices_blueprint.detail_set', set_id=price_obj.set_id))


def get_price_obj(price_id):
    price_obj = database.col_prices.find_one({'_id': price_id})  # dict
    data = json.loads(json_util.dumps(price_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print(price_obj)
    return price_obj


def price_detail(request, price_id, g_user_flask):
    if request.method == 'POST':
        update_price(request, price_id, g_user_flask)
    context = {
        'price': get_price_obj(price_id),
        'priceType': list(priceType),
    }
    return render_template('prices/price_detail.html', context=context)
