import json
from datetime import date
from types import SimpleNamespace

from bson import json_util
from flask import request, render_template, url_for, redirect

from .specific_methods import method_of_filters
from ..db import database


def list_orders():
    all_orders = database.col_orders.find()  # { 'DateCreate: {gt: ''}' ; orderStatus: })
    if request.method == 'POST':
        find_arguments = method_of_filters(request)
        # parse
        all_orders = database.col_orders.find(find_arguments)
    orders_list = []
    count_orders = 0
    distinctCarwashId = []
    for count_orders, i in enumerate(list(all_orders)[::-1], 1):
        # count_orders += 1
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        # order_obj = json.loads(data, object_hook=lambda d: Order(**d))
        order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print(vars(order_obj))
        orders_list.append(order_obj)

        if order_obj is not None and order_obj.CarWashId not in distinctCarwashId:
            distinctCarwashId.append(order_obj.CarWashId)
    print('ORDERS_LIST: ', orders_list)
    # mongo find by filter in () // projections
    carwashes_names = []
    carwashes = database.col_carwashes.find({"Id": {"$in": distinctCarwashId}}, {"Id": 1, "Name": 1})
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
        'admin/orders_list.html',
        context=context
    )


def delete_order(order_id):
    database.col_orders.delete_one({'_id': order_id})
    print(f'User {order_id} deleted successfully')
    return redirect(url_for('admin_blueprint.orders'))
