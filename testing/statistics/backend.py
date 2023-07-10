from flask import render_template

from flask import Flask, Markup, render_template
from ..db import database
from datetime import datetime, timedelta

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
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


def try_shit():
    message = "################################ \n"

    start_time = str(datetime.now())

    print('start_time', type(start_time), start_time)
    pipeline = [
        # {"$match": {"DateCreateMy": {"$gte": start_time}}},
        {"$group": {"_id": "$Status",
                    # "CarWashId": "$CarWashId",
                    "total": {"$sum": "$Sum"},
                    "date": {"_id": "$DateCreate"},
                    "count": {"$sum": 1}}}
    ]
    result = database.col_orders.aggregate(pipeline)
    # Выводим результаты
    message += "Сводка статусов заказов за все время:\n"
    amount_of_orders = 0
    for doc in result:
        print(doc)
        # message += f"{doc['CarWashId']}:\n"
        message += f"""\n{doc['_id']} -> {doc['count']} шт. = {doc['total']} руб.\n"""
        message += '\n'
        amount_of_orders += int(doc['count'])
    message += str(amount_of_orders)
    message += '\n'
    message += "################################"
    print(message)


def get_statistics(g_user_flask):
    try_shit()

    context = {
        'max': 20,
        'labels': labels,
        'values': values,
        'title': 'Все заказы за весь период',
        'chart': {

        }
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