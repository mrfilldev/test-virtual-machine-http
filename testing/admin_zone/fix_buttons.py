import json
from datetime import datetime
from types import SimpleNamespace

import pytz
from bson import json_util
from dateutil.parser import parse
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

    carwashes = database.col_carwashes.find({'network_id': '3a81c491fa9245dc9139049f9885ef57'})
    for carwash in carwashes:
        data = json.loads(json_util.dumps(carwash))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('carwash_obj: ', carwash_obj)
        database.col_carwashes.update_one({'_id': carwash_obj._id}, {"$set": {
            "Price": '',  # '6265a8cb8aab49a6b9407256c1726441',
        }})

    return redirect(url_for('admin_blueprint.admin_main'))


def remake_prices_to_set():
    prices_list = []
    prices = database.col_prices.find({})
    for price in prices:
        data = json.loads(json_util.dumps(price))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('price_obj: ', price_obj)
        setattr(price_obj, "status", 'turn_off')
        prices_list.append(price_obj)
        database.col_prices.update_one({'_id': price_obj._id}, {"$set": {
            "set_id": '6265a8cb8aab49a6b9407256c1726441',
        }})
    print('prices_list: ', prices_list)

    return redirect(url_for('admin_blueprint.admin_main'))


def prices_to_active():
    prices = database.col_prices.find({})
    for price in prices:
        data = json.loads(json_util.dumps(price))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('price_obj: ', price_obj)
        database.col_prices.update_one({'_id': price_obj._id}, {"$set": {
            "status": 'active',
        }})

    return redirect(url_for('admin_blueprint.admin_main'))


def set_all_prices_attr_price_types():
    prices = database.col_prices.find({})
    for price in prices:
        data = json.loads(json_util.dumps(price))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('price_obj: ', price_obj)
        database.col_prices.update_one({'_id': price_obj._id}, {"$set": {
            "priceType": 'main_carwash',
        }})
    return redirect(url_for('admin_blueprint.admin_main'))


def set_all_carwash_full_type():
    carwashes = database.col_carwashes.find({})
    for carwash in carwashes:
        data = json.loads(json_util.dumps(carwash))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('carwash_obj: ', carwash_obj)
        database.col_carwashes.update_one({'_id': carwash_obj._id}, {"$set": {
            'IsCarwash': True,
            'IsWheelStation': True,
            'IsDetaling': True,
        }})

    return redirect(url_for('admin_blueprint.admin_main'))


def set_sets_of_prices_to_one_network():
    sets = database.col_sets_of_prices.find({})

    for set in sets:
        data = json.loads(json_util.dumps(set))
        data = json.dumps(data, default=lambda x: x.__dict__)
        set_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('set_obj: ', set_obj)
        database.col_carwashes.update_one({'_id': set_obj._id}, {"$set": {
            'network': '3a81c491fa9245dc9139049f9885ef57'
        }})

    return redirect(url_for('admin_blueprint.admin_main'))


def fix_box_number_value():
    order = database.col_orders.find_one({"_id": "ff9f21d721d64231963f830b29eff141"})

    data = json.loads(json_util.dumps(order))
    data = json.dumps(data, default=lambda x: x.__dict__)
    order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    print('order_obj: ', order_obj)
    database.col_orders.update_one({'_id': order_obj._id}, {"$set": {
        'BoxNumber': 1
    }})

    return redirect(url_for('admin_blueprint.admin_main'))


def fix_orders_fields():
    all_orders = database.col_orders.find({})

    for order in all_orders:
        data = json.loads(json_util.dumps(order))
        data = json.dumps(data, default=lambda x: x.__dict__)
        order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('order_obj: ', order_obj)
        database.col_orders.update_one({'_id': order_obj._id}, {"$set": {
            "order_user_name": '',
            "phone_number": '',
            "order_basket": '',
        }})
    return redirect(url_for('admin_blueprint.admin_main'))


def fix_sets():
    set_6265a8cb8aab49a6b9407256c1726441 = database.col_sets_of_prices.find_one(
        {'_id': '6265a8cb8aab49a6b9407256c1726441'})
    data = json.loads(json_util.dumps(set_6265a8cb8aab49a6b9407256c1726441))
    data = json.dumps(data, default=lambda x: x.__dict__)
    set_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    print('order_obj: ', set_obj)
    database.col_sets_of_prices.update_one({'_id': set_obj._id}, {"$set": {
        "network": '3a81c491fa9245dc9139049f9885ef57',
    }})

    set_e0df3de573e2421a9220ed952dc04808 = database.col_sets_of_prices.find_one(
        {'_id': 'e0df3de573e2421a9220ed952dc04808'})
    data = json.loads(json_util.dumps(set_e0df3de573e2421a9220ed952dc04808))
    data = json.dumps(data, default=lambda x: x.__dict__)
    set_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    print('order_obj: ', set_obj)
    database.col_sets_of_prices.update_one({'_id': set_obj._id}, {"$set": {
        "network": '3a81c491fa9245dc9139049f9885ef57',
    }})
    return redirect(url_for('admin_blueprint.admin_main'))


def fix_date_users():
    all_users = database.col_users.find({})

    for user in all_users:
        data = json.loads(json_util.dumps(user))
        data = json.dumps(data, default=lambda x: x.__dict__)
        user_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        # print(user_obj.date_registered, parse(user_obj.date_registered), type(parse(user_obj.date_registered)), parse(user_obj.date_registered).isoformat())
        database.col_users.update_one({'_id': user_obj._id}, {"$set": {
            "date_registered": parse(user_obj.date_registered).isoformat(),
        }})
    return redirect(url_for('admin_blueprint.admin_main'))


import datetime
import json


def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()


def fix_date_orders():
    from bson.codec_options import CodecOptions
    import bson
    import collections

    all_orders = database.col_orders.find({})

    for order in all_orders:
        try:
            print('\norder: ', order)
            # Serialize ``obj`` to a JSON formatted ``str``.
            test_obj = json.loads(json_util.dumps(order), object_hook=lambda obj: obj)
            print('\ntest_obj: ', test_obj)
            # Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance containing a JSON document) to a Python
            # object.
            test_obj = json.dumps(test_obj, default=default)

            order_obj = json.loads(test_obj, object_hook=lambda d: SimpleNamespace(**d), default=default)
            print('\norder_obj: ', order_obj)
            print('\n')

            # print('order: ', order)
            #
            # order_obj = SimpleNamespace(**order)
            # print('order_obj: ', order_obj)
            # print('\nbson.encode(order): ', bson.encode(order))
            # print('\nbson.decode(data): ', bson.decode(order))
            # options = CodecOptions(document_class=collections.Simple)
            # decoded_doc = bson.decode(bson.encode(order), codec_options=options)
            # print('\ndecoded_doc: ', decoded_doc, type(decoded_doc))
        except Exception as e:
            print(e)

    return redirect(url_for('admin_blueprint.admin_main'))

    # print(type(order['DateCreate']))
    # print(order['DateCreate'])
    # print('type(test_obj.DateCreate): ', type(test_obj.DateCreate))
    # print('type(test_obj["DateCreate"]): ', type(test_obj['DateCreate']))
    #
    # for order in all_orders:
    #     data = json.loads(json_util.dumps(order))
    #     data = json.dumps(data, default=lambda x: x.__dict__)
    #     order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d), default=default)
    #     try:
    #         print(type(order_obj.DateCreate), type(order_obj.DateCreate), type(order_obj.DateCreate))
    #         print(order_obj.DateCreate, order_obj.DateStart, order_obj.DateEnd)
    #     except Exception as e:
    #         pass
