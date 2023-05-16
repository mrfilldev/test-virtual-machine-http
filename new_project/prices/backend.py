import json
from types import SimpleNamespace

from bson import json_util

from ..db import database


def get_prices_obj_list():
    prices = database.col_prices.find({})
    prices_list = []

    for i in list(prices):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        prices_list.append(price_obj)
    return prices_list
