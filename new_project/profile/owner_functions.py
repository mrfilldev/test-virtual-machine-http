import json
from types import SimpleNamespace

from bson import json_util
from flask import render_template

from ..db import database


def get_carwashes(g):
    network = g.user_db['networks'][0]
    all_carwashes = database.col_carwashes.find({'network_id': network})

    carwashes_list = []
    for count_carwashes, i in enumerate(list(all_carwashes)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        carwashes_list.append(carwash_obj)

    return carwashes_list


def get_carwash_analys(carwashes):
    analys_dict = {}


    return analys_dict


def render_profile_owner(g):
    """
    вывод таблицы с показателями моек за месяц и сегодняшний день
    -получить мойки пользователя
    -по каждой мойке получить список заказов с подсчетом суммы за месяц и сегодняшний день
    """
    carwashes = get_carwashes(g)
    carwash_analys_dict = get_carwash_analys(carwashes)

    context = {}
    return render_template('profile/profile_owner.html', context=context)

#
# network = g.user_db['networks'][0]
# all_carwashes = database.col_carwashes.find({'network_id': network})
# print('network:', network)
# network = database.col_networks.find({'_id': network})
# data = json.loads(json_util.dumps(network))
# data = json.dumps(data, default=lambda x: x.__dict__)
# network_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))[0]  # SimpleNamespace
# print('network_obj:', network_obj)
#
# print('network:', all_carwashes)
# carwashes = []
# for i in all_carwashes:
#     data = json.loads(json_util.dumps(i))
#     data = json.dumps(data, default=lambda x: x.__dict__)
#     carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
#     print('carwash_obj:', carwash_obj)
#     carwashes.append(carwash_obj._id)
# print('carwashes: ', carwashes)
# orders_of_network = database.col_orders.find({'CarWashId': {'$in': carwashes}})
# print('orders_of_network:', orders_of_network)
#
# orders_list = []
# count_orders = 0
# distinctCarwashId = []
# for count_orders, i in enumerate(list(orders_of_network)[::-1], 1):
#     # count_orders += 1
#     print(i)
#     data = json.loads(json_util.dumps(i))
#     data = json.dumps(data, default=lambda x: x.__dict__)
#     # order_obj = json.loads(data, object_hook=lambda d: Order(**d))
#     order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
#     orders_list.append(order_obj)
#
#     if hasattr(order_obj, 'CarWashId') and order_obj.CarWashId not in distinctCarwashId:
#         distinctCarwashId.append(order_obj.CarWashId)
#
# # mongo find by filter in () // projections
# carwashes_names = []
# carwashes = database.col_carwashes.find({"_id": {"$in": distinctCarwashId}}, {"_id": 1, "Name": 1})
# for i in carwashes:
#     data = json.loads(json_util.dumps(i))
#     data = json.dumps(data, default=lambda x: x.__dict__)
#     carwash = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
#     carwashes_names.append(carwash)
# today = date.today()
# context = {
#     'orders_list': orders_list,
#     'count_orders': count_orders,
#     'carwashes': carwashes_names,
#     'date': today
# }
#
# return render_template(
#     'orders/orders_list.html',
#     context=context
# )
# else:
# return abort(404)
#
#
# def owner_order_detail(order_id):
#     order_obj = database.col_orders.find_one({'_id': order_id})  # dict
#     data = json.loads(json_util.dumps(order_obj))
#     data = json.dumps(data, default=lambda x: x.__dict__)
#     order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
#     print('order_obj: \n', order_obj)
#     carwash = get_carwash_obj(order_obj)
#
#     context = {
#         'order': order_obj,
#         'carwash': carwash
#     }
#     return render_template(
#         'orders/order_detail.html',
#         context=context
#     )
#
#
# def get_carwash_obj(order_obj):
#     try:
#         carwash_obj = database.col_carwashes.find_one(order_obj.CarWashId)
#         data = json.loads(json_util.dumps(carwash_obj))
#         data = json.dumps(data, default=lambda x: x.__dict__)
#         carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
#         print('carwash_obj: \n', carwash_obj)
#         return carwash_obj
#     except Exception as error:
#         return None
