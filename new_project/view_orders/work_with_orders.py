import json
from datetime import date
from types import SimpleNamespace

from bson import json_util
from flask import redirect, url_for, abort, render_template, request

from ..db import database
from ..configuration.config import Sqs_params

client = Sqs_params.client
queue_url = Sqs_params.queue_url


def list_orders(g):
    if 'networks' in g.user_db:
        network = g.user_db['networks'][0]
        print('network:', network)
        all_carwashes = database.col_carwashes.find({'network_id': network})
        print('network:', all_carwashes)
    elif g.user_db['role'] == 'admin':
        all_carwashes = database.col_carwashes.find({})
    else:
        return abort(404)
    carwashes = []
    for i in all_carwashes:
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('carwash_obj:', carwash_obj)
        carwashes.append(carwash_obj._id)
    print('carwashes: ', carwashes)
    orders_of_network = database.col_orders.find({'CarWashId': {'$in': carwashes}})
    print('orders_of_network:', orders_of_network)

    orders_list = []
    count_orders = 0
    distinctCarwashId = []
    for count_orders, i in enumerate(list(orders_of_network)[::-1], 1):
        # count_orders += 1
        print(i)
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        # order_obj = json.loads(data, object_hook=lambda d: Order(**d))
        order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        orders_list.append(order_obj)

        if hasattr(order_obj, 'CarWashId') and order_obj.CarWashId not in distinctCarwashId:
            distinctCarwashId.append(order_obj.CarWashId)

    # mongo find by filter in () // projections
    carwashes_names = []
    carwashes = database.col_carwashes.find({"_id": {"$in": distinctCarwashId}}, {"_id": 1, "Name": 1})
    for i in carwashes:
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        carwashes_names.append(carwash)

    request_xhr_key = request.headers.get('X-Requested-With')
    if request_xhr_key == 'XMLHttpRequest':
        context = {
            'orders_list': orders_list,
            'count_orders': count_orders,
            'carwashes': carwashes_names,
        }
        return render_template('orders/orders_table.html', context=context)


    today = date.today()
    context = {
        'orders_list': orders_list,
        'count_orders': count_orders,
        'carwashes': carwashes_names,
        'date': today,
    }
    return render_template(
        'orders/orders_list.html',
        context=context
    )



def owner_order_detail(order_id):
    order_obj = database.col_orders.find_one({'_id': order_id})  # dict
    data = json.loads(json_util.dumps(order_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print('order_obj: \n', order_obj)
    carwash = get_carwash_obj(order_obj)

    context = {
        'order': order_obj,
        'carwash': carwash
    }
    return render_template(
        'orders/order_detail.html',
        context=context
    )


def get_carwash_obj(order_obj):
    try:
        carwash_obj = database.col_carwashes.find_one(order_obj.CarWashId)
        data = json.loads(json_util.dumps(carwash_obj))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
        print('carwash_obj: \n', carwash_obj)
        return carwash_obj
    except Exception as error:
        return None


def accept_order(order_id):
    print(f'Order {order_id} is accepting')
    order_obj = database.col_orders.find_one({'_id': order_id})  # dict
    dict_to_sqs = {'order': str(order_obj), 'task': 'changeStatus', 'new_status': 'Accepted'}

    print(
        'Sending order to accept:...',
        client.send_message(
            QueueUrl=queue_url,
            MessageBody=str(dict_to_sqs)
        )
    )


def complete_order(order_id):
    print(f'Order {order_id} is accepting')
    order_obj = database.col_orders.find_one({'_id': order_id})  # dict
    dict_to_sqs = {'order': str(order_obj), 'task': 'changeStatus', 'new_status': 'Completed'}
    print(
        'Sending order to complete:...',
        client.send_message(
            QueueUrl=queue_url,
            MessageBody=str(dict_to_sqs)
        )
    )


def cancel_order(order_id):
    print(f'Order {order_id} is accepting')
    order_obj = database.col_orders.find_one({'_id': order_id})  # dict
    dict_to_sqs = {'order': str(order_obj), 'task': 'changeStatus', 'new_status': 'Canceled'}
    print(
        'Sending order to complete:...',
        client.send_message(
            QueueUrl=queue_url,
            MessageBody=str(dict_to_sqs)
        )
    )
