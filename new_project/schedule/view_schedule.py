import json
from datetime import datetime, timedelta, date
from types import SimpleNamespace

from bson import json_util
from flask import render_template, jsonify

from new_project.db import database
from new_project.db.models import TestScheduleOrder


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def get_orders(carwash_id):  # 7810324c8fea4af8bc3c3d6776cfc494
    orders = database.col_orders.find({"CarWashId": carwash_id})
    events_list = []
    for i in orders:
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('order_obj:', order_obj)
        events_list.append({
            'title': 'Заказ',
            'start': order_obj.DateCreate.replace('Z', ''),
            'resourceId': order_obj.BoxNumber,
        })
    return events_list


def view_schedule(g_user_flask):
    # Pass schedule data to template
    events = [
        {
            'title': 'Заказ',
            'start': '2023-05-03T16:00:00',
            'end': '2023-05-03T17:30:00',
            'description': 'Мойка "кузов"',
            'resourceId': 'a',
            'carNumber': 'A111AA750'
        },
        {
            'title': 'Заказ',
            'start': '2023-05-03T17:30:00',
            'end': '2023-05-03T17:50:00',
            'description': 'Мойка "кузов+коврики"',
            'resourceId': 'b',
            'carNumber': 'B222AA750'
        },
        {
            'title': 'Заказ',
            'start': '2023-05-03T18:15:00',
            'end': '2023-05-03T19:00:00',
            'description': 'Мойка "кузов+коврики+воск"',
            'resourceId': 'c'
        }
    ]
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
    date_today = '2023-05-03'
    now_iso = datetime.now().isoformat()

    events += get_orders('7810324c8fea4af8bc3c3d6776cfc494')
    context = {
        'orders': events,
        'boxes': resources,
        'carwash_start_time': carwash_start_time,
        'carwash_end_time': carwash_end_time,
        'date_today': date_today,
        'now_iso': now_iso
    }
    return render_template('schedule/view_schedule.html', context=context)


def create_carwash(request):
    print('\n################################################################\n')
    dict_of_form = request.form.to_dict(flat=False)
    print(dict_of_form)
    print('################################################################\n')

    for k, v in dict_of_form.items():
        print(k, '-> ', v)

    print('\n################################################################\n')

    data = request.form.to_dict()
    print(data)
    # обработка данных и формирование ответа
    response = {'status': 'success'}
    return jsonify(response)
