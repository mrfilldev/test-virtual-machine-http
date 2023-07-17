import calendar
import json

from flask import render_template

from flask import Flask, Markup, render_template
from ..db import database
from datetime import datetime, timedelta
import locale

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


def get_statistics(g_user_flask):
    # research_by_date = group_by_date()
    research_by_status = group_by_status()
    statuses = rus_arr_statuses(research_by_status)
    print('statuses: ', statuses)
    values = int_arr_values(research_by_status)
    print('values: ', values)
    print('#######################\n')
    print('#######################\n')
    print(locale.getlocale())
    print(testingo_of_chats_res(), '\n')
    dict_amount_months = testingo_of_chats_res()
    print(list(dict_amount_months.keys()))
    print(list(dict_amount_months.values()))

    context = {
        'max': max(values),
        'labels': list(dict_amount_months.keys()),
        'values': list(dict_amount_months.values()),
        'title': 'Все заказы за весь период',
        'research_by_status': research_by_status,
        'research_by_date': statuses,
        'chart': {}
    }
    return render_template(
        'statistics/show_statistics.html',
        context=context
    )


def testingo_of_chats_res():
    # Формирование агрегационного запроса
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

    # Выполнение агрегации и получение результата
    result = list(database.col_orders.aggregate(pipeline))

    result_dict_pretty_format = {}
    # Вывод результатов
    for item in result:
        year = item['year']
        month = item['month']
        count = item['count']
        # date = datetime(year, month, 1).strftime('%b %Y').capitalize()
        result_dict_pretty_format[f'{months[month]}'] = count
        print(f'{year} {months[month - 1]}: {count} событий')
    print('result_dict_pretty_format: ', result_dict_pretty_format)
    return result_dict_pretty_format
