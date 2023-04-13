import json
from datetime import date
from types import SimpleNamespace

from bson import json_util
from flask import redirect, url_for, abort, render_template

from ..db import database


def list_orders(g):
    if 'networks' in g.user_db:
        network = g.user_db['networks'][0]
        all_carwashes = database.col_carwashes.find({'network_id': network})
        print('network:', network)
        network = database.col_networks.find({'_id': network})
        data = json.loads(json_util.dumps(network))
        data = json.dumps(data, default=lambda x: x.__dict__)
        network_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))[0]  # SimpleNamespace
        print('network_obj:', network_obj)

        print('network:', all_carwashes)
        carwashes = []
        for i in all_carwashes:
            data = json.loads(json_util.dumps(i))
            data = json.dumps(data, default=lambda x: x.__dict__)
            carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
            print('carwash_obj:', carwash_obj)
            carwashes.append(carwash_obj.network_id)
        print(carwashes)
        orders_of_network = database.col_orders.find({'CarWashId': {'$in': carwashes}})
        print('orders_of_network:', orders_of_network)

        orders_list = []
        count_orders = 0
        distinctCarwashId = []
        for count_orders, i in enumerate(list(orders_of_network)[::-1], 1):
            # count_orders += 1
            data = json.loads(json_util.dumps(i))
            data = json.dumps(data, default=lambda x: x.__dict__)
            # order_obj = json.loads(data, object_hook=lambda d: Order(**d))
            order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
            print(vars(order_obj))
            orders_list.append(order_obj)

            if hasattr(order_obj, 'CarWashId') and order_obj.CarWashId not in distinctCarwashId:
                distinctCarwashId.append(order_obj.CarWashId)
        print('ORDERS_LIST: ', orders_list)
        # mongo find by filter in () // projections
        carwashes_names = []
        carwashes = database.col_carwashes.find({"_id": {"$in": distinctCarwashId}}, {"_id": 1, "Name": 1})
        for i in carwashes:
            data = json.loads(json_util.dumps(i))
            data = json.dumps(data, default=lambda x: x.__dict__)
            carwash = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
            carwashes_names.append(carwash)
        print(carwashes_names)
        for i in carwashes_names:
            print('carwashes_names: ', i)

        today = date.today()
        context = {
            'orders_list': orders_list,
            'count_orders': count_orders,
            'carwashes': carwashes_names,
            'date': today
        }
        print('CONTEXT: ', context)
        return render_template(
            'orders/orders_list.html',
            context=context
        )
    else:
        return abort(404)
