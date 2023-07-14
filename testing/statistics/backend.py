import json

from flask import render_template

from flask import Flask, Markup, render_template
from ..db import database
from datetime import datetime, timedelta

labels = [
    'Заказ создан',
    'Заказ выполнен',
    'Заказ отменен мойкой',
    'Заказ отменен пользователем',
    'Заказ не актуален',
    'Заказ не выполнен'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


def translate_statuses(category):
    match category:
        case 'OrderCreated':
            return 'Заказ создан'
        case 'Completed':
            return 'Заказ выполнен'
        case 'Accepted':
            return 'Заказ принят'
        case 'LocalOrder':
            return 'Локальный заказ'
        case 'StationCanceled':
            return 'Заказ отменен мойкой'
        case 'UserCanceled':
            return 'Заказ отменен пользователем'
        case 'Expire':
            return 'Заказ не актуален'
        case 'SystemAggregator_Error':
            return 'Заказ не выполнен'
        case _:
            return category


def group_by_status():
    pipeline_by_status = [{
        "$group": {
            "_id": "$Status",
            "total": {"$sum": "$Sum"},
            "count": {"$sum": 1}
        }
    }]
    result = database.col_orders.aggregate(pipeline_by_status)
    amount_of_orders = 0
    status_dictionary = {}  # словарь результата поиска статус:кол-во
    # status_dictionary = {}  # словарь результата поиска статус:объем средств
    for doc in result:
        status_dictionary[doc['_id']] = doc['count']
        amount_of_orders += int(doc['count'])

    for k, v in status_dictionary.items():
        print(f'{k}:{v}\n')
    return status_dictionary


def group_by_date():
    message = "################################ \n"
    pipline_date = [{
        "$group": {
            "_id": {
                "$dayOfYear": "$DateCreate"
            },
            "amount": {"$sum": 1}
        }
    }]
    result = database.col_orders.aggregate(pipline_date)
    # Выводим результаты
    amount_of_orders = 0
    for doc in result:
        print(doc)
        # message += f"{doc['CarWashId']}:\n"
        message += f"""\n{doc['_id']} -> {doc['amount']} шт.\n"""
        message += '\n'
        amount_of_orders += int(doc['amount'])
    message += str(amount_of_orders)
    message += '\n'
    message += "################################"
    print(message)
    return message


def rus_arr_statuses(dictionary):
    arr = []
    for k, v in dictionary.items():
        print(f'{k}:{v}\n')
        arr.append(translate_statuses(k))
    return arr


def int_arr_values(dictionary):
    arr = []
    for k, v in dictionary.items():
        print(f'{k}:{v}\n')
        arr.append(int(v))
    return arr


def get_statistics(g_user_flask):
    # research_by_date = group_by_date()
    research_by_status = group_by_status()
    statuses = rus_arr_statuses(research_by_status)
    print('statuses: ', statuses)
    values = int_arr_values(research_by_status)
    print('values: ', values)

    context = {
        'max': max(values),
        'labels': statuses,
        'values': values,
        'title': 'Все заказы за весь период',
        'research_by_status': research_by_status,
        'research_by_date': statuses,
        'chart': {}
    }
    return render_template(
        'statistics/show_statistics.html',
        context=context
    )

# print("################################")
# start_time = str(datetime.now())
# print(start_time)
# message += "\n За последние 15 минут: \n"
# now = datetime.now()
# interval = now - timedelta(minutes=15)
# print(interval)
# агрегация заказов за последние 15 минут
# start_time = datetime.utcnow() - timedelta(minutes=15)
# print(start_time)
# message += '\n'
# message += "################################"
#
# print("################################")
# print(message)
# выполнить агрегацию
# query = {
#     'DateCreate': {'$gt': start_time.isoformat()}
# }
# pipeline = [
#     {
#         '$match': {
#             'DateCreate': {'$gt': start_time.isoformat()}
#         }
#     },
#     {
#         '$group': {
#             '_id': '$Status',
#             'count': {'$sum': 1},
#             "total": {"$sum": "$Sum"},
#         }
#     }
# ]
# message += '\n ПОЛУЧАЕМЫЙ ОБЪЕКТ АГГРЕГАЦИИ: \n'
# amount_of_orders = 0
# for doc in result:
#     print(doc)
#     message += str(doc)
#     message += f"""\n{doc['_id']} -> {doc['count']} шт. = {doc['total']} руб.\n"""
#     amount_of_orders += doc['count']
