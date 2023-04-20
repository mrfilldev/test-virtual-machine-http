import json
from datetime import date
from types import SimpleNamespace

import pymongo
from bson import json_util
from flask import redirect, url_for, abort, render_template, request

from ..db import database
from ..configuration.config import Sqs_params

client = Sqs_params.client
queue_url = Sqs_params.queue_url

page_size = 10


def list_orders(g, p):
    if 'networks' in g.user_db:
        network = g.user_db['networks'][0]
        print('network:', network)

        search = {'network_id': network}
    elif g.user_db['role'] == 'admin':

        search = {}
    else:
        return abort(404)
    skip = page_size * p
    # limit = page_size * p + page_size
    # print('limit:', limit)
    print('skip:', skip)
    orders_count = database.col_orders.count_documents(search)  # skip=skip)
    sort = [("DateCreate", pymongo.DESCENDING)]
    print('orders_count:', orders_count)
    orders = database.col_orders.find(search).sort(sort).skip(skip).limit(page_size)

    orders_list = []
    distinctCarwashId = []
    for i in orders:
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('order_obj:', order_obj)
        orders_list.append(order_obj)

        if order_obj.CarWashId not in distinctCarwashId:
            distinctCarwashId.append(order_obj.CarWashId)

    # mongo find by filter in () // projections
    carwashes_names = []
    carwashes = database.col_carwashes.find({"_id": {"$in": distinctCarwashId}})
    for i in carwashes:
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        carwashes_names.append(carwash)

    request_xhr_key = request.headers.get('X-Requested-With')
    if request_xhr_key == 'XMLHttpRequest':
        context = {
            'orders_list': orders_list,
            'count_orders': orders_count,
            'carwashes': carwashes_names,
        }
        return render_template('orders/orders_table.html', context=context)

    today = date.today()
    context = {
        'orders_list': orders_list,
        'count_orders': orders_count,
        'carwashes': carwashes_names,
        'date': today
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
