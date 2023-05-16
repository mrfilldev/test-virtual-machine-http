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


def show_prices_list(carwash_id):
    context = {
        'prices': get_prices_obj_list(),
        'enum_list': list(CategoryAuto)
    }
    return render_template('prices/price_list.html', context=context)
