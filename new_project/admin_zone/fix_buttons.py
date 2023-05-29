import json
from types import SimpleNamespace

from bson import json_util
from flask import url_for, redirect

from ..db import database


def fix_network_id_in_orders():
    all_orders = database.col_orders.find({})

    for order in all_orders:
        data = json.loads(json_util.dumps(order))
        data = json.dumps(data, default=lambda x: x.__dict__)
        order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('order_obj: ', order_obj)
        database.col_orders.update_one({'_id': order_obj._id}, {"$set": {
            "Category": 'Compact',
        }})
    return redirect(url_for('admin_blueprint.admin_main'))


def back_carwashes_refresh_prices():
    prices_list = []

    prices = database.col_prices.find({})
    for price in prices:
        data = json.loads(json_util.dumps(price))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('price_obj: ', price_obj)
        setattr(price_obj, "status", 'turn_off')
        prices_list.append(price_obj)
    print('prices_list: ', prices_list)

    carwashes = database.col_carwashes.find({})
    for carwash in carwashes:
        data = json.loads(json_util.dumps(carwash))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('carwash_obj: ', carwash_obj)
        database.col_carwashes.update_one({'_id': carwash_obj._id}, {"$set": {
            "Price": [],
        }})

    return redirect(url_for('admin_blueprint.admin_main'))


def clear_sets():
    database.col_sets_of_prices.delete_one({'_id': '6474c531578b8db9ff8f68cd'})
    return redirect(url_for('admin_blueprint.admin_main'))
