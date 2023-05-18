import json
from types import SimpleNamespace

from bson import json_util
from flask import render_template

from ..db import database
from ..db.models import CategoryAuto


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


def show_prices_list(carwash_id):
    context = {
        'carwash': get_carwash_obj(carwash_id),
        'prices': get_prices_obj_list(),
        'enum_list': list(CategoryAuto)
    }
    return render_template('prices/price_list.html', context=context)


def get_price_info(price_id):
    price_obj = database.col_carwashes.find_one({'_id': price_id})  # dict
    data = json.loads(json_util.dumps(price_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    context = {
        'price': price_obj,
        'enum_list': list(CategoryAuto),
    }
    return render_template('view_carwash/carwash_detail_price.html', context=context)
