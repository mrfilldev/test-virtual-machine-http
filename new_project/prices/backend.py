import json
import uuid
from types import SimpleNamespace

from bson import json_util
from flask import render_template, request, jsonify

from ..db import database
from ..db.models import CategoryAuto, SetOfPrices, PriceOfSet, CostIdSum


def get_prices_obj_list():
    prices = database.col_prices.find({})
    prices_list = []

    for i in list(prices):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        prices_list.append(price_obj)
    return prices_list


def get_carwash_obj(carwash_id):
    carwash_obj = database.col_carwashes.find_one({'_id': carwash_id})  # dict
    data = json.loads(json_util.dumps(carwash_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    return carwash_obj


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


def show_list_sets_prices():
    all_sets = database.col_sets_of_prices.find({})
    sets_serialized = serializing_sets_collection(all_sets)
    print(sets_serialized)
    context = {
        'prices': get_prices_obj_list(),
        'enum_list': list(CategoryAuto),
        'sets': sets_serialized,
    }
    return render_template('prices/list_sets_price.html', context=context)


def set_create(request):
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
        print(new_set)
        database.col_sets_of_prices.insert_one(new_set)

    response = {'status': 'success'}
    return jsonify(response)


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


def set_detail(request, set_id):
    if request.method == 'POST':
        pass
    set_obj = serializing_set(set_id)
    set_id_prices = find_prices_with_set_id(set_id)
    context = {
        'set_prices': set_id_prices,
        'set': set_obj,
        'enum_list': list(CategoryAuto),
    }
    return render_template('prices/set_detail.html', context=context)


def create_price(request, set_id):
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

        for i in list(CategoryAuto):
            categoryPrice.append(CostIdSum(i.name, form[str(i.name)]))

        new_price = PriceOfSet(id, set_id, name, description, categoryPrice, costType)

        print(new_price.categoryPrice)
        print(new_price.set_id)
        for i in new_price.categoryPrice:
            print(f'{i.category} -> {i.sum}')

        # запись в бд
        new_price = eval(json.dumps(new_price, default=lambda x: x.__dict__))
        print(new_price)
        print(type(new_price))
        database.col_prices.insert_one(new_price)

    response = {'status': 'success'}
    return jsonify(response)


def update_price(request, price_id):
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
        'status': 'active',
    }}
    new_price = database.col_prices.update_one(price_id, set_fields)
    print('UPDATE FIELDS: ', set_fields)
    print('UPDATE DATA: ', new_price)


def hide_price(price_id):
    price_id = {'_id': price_id}
    set_fields = {'$set': {
        'status': 'turn_off',
    }}
    new_price = database.col_prices.update_one(price_id, set_fields)
    print('UPDATE FIELDS: ', set_fields)
    print('UPDATE DATA: ', new_price)


def get_price_obj(price_id):
    price_obj = database.col_prices.find_one({'_id': price_id})  # dict
    data = json.loads(json_util.dumps(price_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print(price_obj)
    return price_obj


def price_detail(request, price_id):
    if request.method == 'POST':
        update_price(request, price_id)
    context = {
        'price': get_price_obj(price_id),
    }
    return render_template('prices/price_detail.html', context=context)
