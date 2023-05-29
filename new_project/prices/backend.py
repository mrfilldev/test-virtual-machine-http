import json
import uuid
from types import SimpleNamespace

from bson import json_util
from flask import render_template, request, jsonify

from ..db import database
from ..db.models import CategoryAuto, SetOfPrices


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
    data = json.loads(json_util.dumps(i))
    data = json.dumps(data, default=lambda x: x.__dict__)
    set_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    set_obj.append(set_obj)
    print(set_obj, '\n')
    return set_obj


def show_list_sets_prices():
    all_sets = database.col_sets_of_prices.find({})
    sets_serialized = serializing_sets_collection(all_sets)

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


def set_detail(request, set_id):
    if request.method == 'POST':
        pass
    set = database.col_sets_of_prices.find({'_id': set_id})
    set_obj = serializing_set(set)
    context = {
        'set': set_obj,
        'enum_list': list(CategoryAuto),
    }
    return render_template('prices/set_detail.html', context=context)
