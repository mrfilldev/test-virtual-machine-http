import calendar
import json

from flask import render_template, abort

from flask import Flask, Markup, render_template
from ..db import database
from datetime import datetime, timedelta
import locale
# Importing required functions
from flask import Flask, render_template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import BoxZoomTool, PanTool, ResetTool


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

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

months = [
    "Январь", "Февраль", "Март", "Апрель",
    "Май", "Июнь", "Июль", "Август",
    "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
]


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


def amount_orders_per_months(g_user_flask):
    if g_user_flask.user_db['role'] == 'network_owner':
        network_id = g_user_flask.user_db['networks'][0]
        print('network_id: ', network_id)
        pipeline = [
            {
                '$match': {
                    'network_id': {'$eq': network_id}
                }
            },
            {
                '$group': {
                    '_id': {
                        'year': {'$year': '$DateCreate'},
                        'month': {'$month': '$DateCreate'}
                    },
                    'count': {'$sum': 1}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'year': '$_id.year',
                    'month': '$_id.month',
                    'count': 1
                }
            },
            {
                '$sort': {
                    'year': 1,
                    'month': 1
                }
            }
        ]
    elif g_user_flask.user_db['role'] == 'admin':
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'year': {'$year': '$DateCreate'},
                        'month': {'$month': '$DateCreate'}
                    },
                    'count': {'$sum': 1}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'year': '$_id.year',
                    'month': '$_id.month',
                    'count': 1
                }
            },
            {
                '$sort': {
                    'year': 1,
                    'month': 1
                }
            }
        ]
    else:
        return abort(404)
    # Выполнение агрегации и получение результата
    result = list(database.col_orders.aggregate(pipeline))
    result_dict_pretty_format = {}
    # Вывод результатов
    for item in result:
        year = item['year']
        month = item['month']
        count = item['count']
        # date = datetime(year, month, 1).strftime('%b %Y').capitalize()
        result_dict_pretty_format[f'{months[month - 1]}'] = count
        print(f'{year} {months[month - 1]}: {count} событий')
    return result_dict_pretty_format


def get_statistics(g_user_flask):
    # Defining Chart Data
    language = [
        'Python', 'Java', 'JavaScript', 'C#', 'PHP', 'C/C++',
        'R', 'Objective-C', 'Swift', 'TypeScript', 'Matlab',
        'Kotlin', 'Go', 'Ruby', 'VBA'
    ]
    popularity = [
        31.56, 16.4, 8.38, 6.5, 5.85, 5.8, 4.08, 2.79, 2.35,
        1.92, 1.65, 1.61, 1.44, 1.22, 1.16
    ]

    dict_amount_months = amount_orders_per_months(g_user_flask)

    # Creating Plot Figure
    p = figure(
        x_range=list(dict_amount_months.keys()),
        height=400,
        title="Кол-во заказов",
        sizing_mode="stretch_width"
    )

    # Defining Plot to be a Vertical Bar Plot
    p.vbar(x=list(dict_amount_months.keys()), top=list(dict_amount_months.values()), width=0.5)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.toolbar_location = None

    # Get Chart Components
    script, div = components(p)

    # Return the components to the HTML template
    context = {
        'script': script,
        'div': div,
    }
    print(context)
    return render_template('statistics/show_statistics.html', context=context)


# def get_statistics(g_user_flask):
#     # research_by_date = group_by_date()
#     research_by_status = group_by_status()
#     statuses = rus_arr_statuses(research_by_status)
#     print('statuses: ', statuses)
#     values = int_arr_values(research_by_status)
#     print('values: ', values)
#     print('#######################\n')
#     print('#######################\n')
#     print(locale.getlocale())
#     print(testingo_of_chats_res(g_user_flask.user_db['networks'][0]), '\n')
#     dict_amount_months = testingo_of_chats_res(g_user_flask.user_db['networks'][0])
#     print(list(dict_amount_months.keys()))
#     print(list(dict_amount_months.values()))
#
#     context = {
#         'max': max(values),
#         'labels': list(dict_amount_months.keys()),
#         'values': list(dict_amount_months.values()),
#         'title': 'Все заказы за весь период',
#         'research_by_status': research_by_status,
#         'research_by_date': statuses,
#         'chart': {},
#         'type': 'bar',
#     }
#     return render_template(
#         'statistics/show_statistics.html',
#         context=context
#     )
