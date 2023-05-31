import json
import uuid
from datetime import datetime, timedelta, date
from types import SimpleNamespace

from bson import json_util
from flask import render_template, jsonify, abort

from new_project.db import database
from new_project.db.models import TestScheduleOrder, Catergory


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def get_orders(carwash_id):  # 7810324c8fea4af8bc3c3d6776cfc494
    orders = database.col_orders.find({'CarWashId': carwash_id})
    events_list = []
    for i in orders:
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('order_obj:', order_obj)
        events_list.append({

            'title': order_obj.CarNumber,

            'order_id': order_obj._id,

            'start': order_obj.DateStart.replace('Z', ''),
            'end': order_obj.DateEnd.replace('Z', ''),
            'date': order_obj.DateCreate,

            'start_format': '' if order_obj.DateStart == '' else datetime.strptime(
                (order_obj.DateStart.replace('Z', '')), "%Y-%m-%dT%H:%M:%S").strftime('%H:%M'),
            'end_format': '' if order_obj.DateEnd == '' else datetime.strptime(
                (order_obj.DateEnd.replace('Z', '')), "%Y-%m-%dT%H:%M:%S").strftime('%H:%M'),
            'date_format': '' if order_obj.DateCreate == '' else datetime.strptime(
                (order_obj.DateCreate.replace('Z', '')).rpartition(':')[0], "%Y-%m-%dT%H:%M").strftime('%Y-%m-%d'),

            'resourceId': (chr(ord('`') + int(order_obj.BoxNumber))),
            'box': order_obj.BoxNumber,
            'carNumber': order_obj.CarNumber,
            'category': '-' if order_obj.Category == '' else order_obj.Category,
            'car_brand': order_obj.CarBrand,
            'car_model': order_obj.CarModel,
        })
        print('start', order_obj.DateStart)
        print('end', order_obj.DateEnd)
        print('date', order_obj.DateCreate)

    print(events_list)
    return events_list


def get_boxes(carwash_obj):
    resources = []
    for i in range(1, len(carwash_obj.Boxes) + 1):
        resources.append(
            {
                'id': chr(ord('`') + i),
                'title': f'Бокс {i}',
            }
        )
    return resources


def get_amount_boxes(carwash_obj):
    return len(carwash_obj.Boxes)


def get_carwash_obj(carwash_id):
    carwash_obj = database.col_carwashes.find_one({'_id': carwash_id})  # dict
    data = json.loads(json_util.dumps(carwash_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print('carwash_obj: ', carwash_obj)
    return carwash_obj


def get_price_list(set_id):
    prices_of_set = []
    prices = database.col_prices.find({'set_id': set_id})  # dict
    for price in prices:
        data = json.loads(json_util.dumps(price))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        prices_of_set.append(price_obj)

    print(prices_of_set)
    return prices_of_set


def view_schedule_of_certain_carwash(request, carwash_id, g_user_flask):
    carwash_obj = get_carwash_obj(carwash_id)

    events = get_orders(carwash_id)
    resources = get_boxes(carwash_obj)

    carwash_start_time = '08:00:00'
    carwash_end_time = '23:00:00'
    date_today = datetime.today().strftime('%Y-%m-%d')

    now_iso = datetime.now().isoformat()

    now_format = (datetime.now() - timedelta(hours=1.5)).strftime('%H:%M:%S')
    print('now_format: ', now_format)

    request_xhr_key = request.headers.get('X-Requested-With')
    if request_xhr_key == 'XMLHttpRequest':
        context = {
            'orders': events,
            'price_list': get_price_list(carwash_obj.Price),
            'boxes': resources,
            'carwash_start_time': carwash_start_time,
            'carwash_end_time': carwash_end_time,
            'date_today': date_today,
            'now_iso': now_iso,
            'scrollToTime': now_format
        }
        return context

    context = {
        'calendar': {
            'orders': events,
            'price_list': get_price_list(carwash_obj.Price),
            'boxes': resources,
            'carwash_start_time': carwash_start_time,
            'carwash_end_time': carwash_end_time,
            'date_today': date_today,
            'now_iso': now_iso,
            'scrollToTime': now_format
        },
        'carwash': carwash_obj,
        'category': Catergory,
        'box': get_amount_boxes(carwash_obj),

    }
    return render_template('schedule/view_schedule.html', context=context)


def create_carwash_order(request, carwash_id):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print(data, carwash_id)
    print('\n################################################################\n')
    # обработка данных
    carwash_obj = get_carwash_obj(carwash_id)

    order_id = uuid.uuid4().hex
    carwash_id = carwash_id
    network_id = carwash_obj.network_id
    box = request.form['box']
    country_region_number = request.form['country_region_number']
    car_brand = request.form['car_brand']
    car_model = request.form['car_model']
    category = request.form['category']

    contract_id = 'OWN'
    sum = 1000.0
    sum_completed = 1000.0
    sum_paid_station_completed = 1000.0
    Status = 'OrderCreated'
    date_created = datetime.now().isoformat()
    date_start = datetime.strptime(request.form['date'] + ' ' + request.form['time_start'],
                                   "%Y-%m-%d %H:%M").isoformat()
    date_end = datetime.strptime(request.form['date'] + ' ' + request.form['time_end'], "%Y-%m-%d %H:%M").isoformat()

    order = {
        '_id': order_id,
        'CarWashId': carwash_id,
        'BoxNumber': box,
        'CarNumber': country_region_number,
        'CarModel': car_model,
        'CarBrand': car_brand,
        'Category': category,
        'ContractId': contract_id,
        'Sum': sum,
        'Status': Status,
        'DateCreate': date_created,
        'DateStart': date_start,
        'DateEnd': date_end,
        'SumCompleted': sum_completed,
        'SumPaidStationCompleted': sum_paid_station_completed,
        'network_id': network_id,
    }

    print('Writing into DB')
    print(order)
    database.col_orders.insert_one(order)

    # формирование ответа
    response = {'status': 'success'}
    return jsonify(response)


def edit_carwash_order(request, carwash_id):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print(data, carwash_id)
    print('\n################################################################\n')

    id_order = {'_id': request.form['order_id']}
    print('id_order: ', request.form['order_id'])
    set_fields = {'$set': {
        'BoxNumber': request.form['box'],
        'CarNumber': request.form['country_region_number'],
        'CarModel': request.form['car_model'],
        'CarBrand': request.form['car_brand'],
        'Category': request.form['category'],
        'ContractId': 'OWN',
        'DateStart': datetime.strptime(request.form['date'] + ' ' + request.form['time_start'],
                                       "%Y-%m-%d %H:%M").isoformat(),
        'DateEnd': datetime.strptime(request.form['date'] + ' ' + request.form['time_end'],
                                     "%Y-%m-%d %H:%M").isoformat(),
    }}
    new_order = database.col_orders.update_one(id_order, set_fields)
    print(" #####  EDITING  #####")
    print('UPDATE FIELDS: ', set_fields)
    print('UPDATE DATA: ', new_order)

    response = {'status': 'success'}
    return jsonify(response)
