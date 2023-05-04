import json
from datetime import datetime, timedelta, date
from types import SimpleNamespace

from bson import json_util
from flask import render_template, jsonify, abort

from new_project.db import database
from new_project.db.models import TestScheduleOrder


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def get_orders(carwash_id):  # 7810324c8fea4af8bc3c3d6776cfc494
    orders = database.col_orders.find({})
    events_list = []
    for i in orders:
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('order_obj:', order_obj)
        events_list.append({
            'title': 'Заказ',
            'start': order_obj.DateCreate.replace('Z', ''),
            'end': order_obj.DateCreate.replace('Z', ''),
            'resourceId': 'a',
            'carNumber': order_obj.ContractId,
        })
    print(events_list)
    return events_list


def view_schedule(g_user_flask):
    # if 'networks' in g_user_flask.user_db:
    #     network = g_user_flask.user_db['networks'][0]
    #     print('network:', network)
    #
    #     search = {'network_id': network}
    # elif g_user_flask.user_db['role'] == 'admin':
    #     search = {}
    # Pass schedule data to template
    resources = [
        {'id': 'a', 'title': 'Бокс 1'},
        {'id': 'b', 'title': 'Бокс 2'},
        {'id': 'c', 'title': 'Бокс 3'},
        {'id': 'd', 'title': 'Бокс 4'},
        {'id': 'e', 'title': 'Бокс 5'},
        {'id': 'f', 'title': 'Бокс 6'},
        {'id': 'g', 'title': 'Бокс 7'},
        {'id': 'h', 'title': 'Бокс 8'},
        {'id': 'i', 'title': 'Бокс 9'},
        {'id': 'j', 'title': 'Бокс 10'},
        {'id': 'k', 'title': 'Бокс 11'},
        {'id': 'l', 'title': 'Бокс 12'},
    ]
    carwash_start_time = '08:00:00'
    carwash_end_time = '23:00:00'
    date_today = datetime.today().strftime('%Y-%m-%d')
    now_iso = datetime.now().isoformat()

    events = get_orders('7810324c8fea4af8bc3c3d6776cfc494')
    context = {
        'orders': events,
        'boxes': resources,
        'carwash_start_time': carwash_start_time,
        'carwash_end_time': carwash_end_time,
        'date_today': date_today,
        'now_iso': now_iso
    }
    return render_template('schedule/view_schedule.html', context=context)


def get_carwash_obj(carwash_id):
    carwash_obj = database.col_carwashes.find_one({'_id': carwash_id})  # dict
    data = json.loads(json_util.dumps(carwash_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print('carwash_obj: ', carwash_obj)
    return carwash_obj


def view_schedule_of_certain_carwash(carwash_id, g_user_flask):
    carwash_obj = get_carwash_obj(carwash_id)

    resources = [
        {'id': 'a', 'title': 'Бокс 1'},
        {'id': 'b', 'title': 'Бокс 2'},
        {'id': 'c', 'title': 'Бокс 3'},
        {'id': 'd', 'title': 'Бокс 4'},
        {'id': 'e', 'title': 'Бокс 5'},
        {'id': 'f', 'title': 'Бокс 6'},
        {'id': 'g', 'title': 'Бокс 7'},
        {'id': 'h', 'title': 'Бокс 8'},
        {'id': 'i', 'title': 'Бокс 9'},
        {'id': 'j', 'title': 'Бокс 10'},
        {'id': 'k', 'title': 'Бокс 11'},
        {'id': 'l', 'title': 'Бокс 12'},
    ]
    carwash_start_time = '08:00:00'
    carwash_end_time = '23:00:00'
    date_today = datetime.today().strftime('%Y-%m-%d')
    now_iso = datetime.now().isoformat()

    events = get_orders(carwash_id)
    context = {
        'orders': events,
        'boxes': resources,
        'carwash_start_time': carwash_start_time,
        'carwash_end_time': carwash_end_time,
        'date_today': date_today,
        'now_iso': now_iso
    }
    return render_template('schedule/view_schedule.html', context=context)


def create_carwash_order(request):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print(data)
    print('\n################################################################\n')
    # обработка данных и формирование ответа
    response = {'status': 'success'}
    return jsonify(response)
