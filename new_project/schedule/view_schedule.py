import json
import uuid
from datetime import datetime, timedelta, date
from types import SimpleNamespace

from bson import json_util
from flask import render_template, jsonify, abort, Response

from new_project.db import database
from new_project.db.models import TestScheduleOrder, Catergory, CategoryAuto, priceType, basketItem

_eng_chars = u"~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
_rus_chars = u"ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
_to_rus = dict(zip(_eng_chars, _rus_chars))
_to_eng = dict(zip(_rus_chars, _eng_chars))


def to_rus(s):
    return u''.join([_to_rus.get(c, c) for c in s])


def to_eng(s):
    return u''.join([_to_eng.get(c, c) for c in s])


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
        if order_obj.ContractId == "YARU":
            events_list.append({
                'title': order_obj.ContractId,
                'order_id': order_obj._id,
                'start': order_obj.DateCreate.replace('Z', ''),
                'date': order_obj.DateCreate,
                'start_format': '' if order_obj.DateCreate == '' else datetime.strptime(
                    ((order_obj.DateCreate.replace('Z', '')).split('.')[0]), "%Y-%m-%dT%H:%M:%S").strftime('%H:%M'),
                'resourceId': (chr(ord('`') + int(order_obj.BoxNumber))),
                'box': order_obj.BoxNumber,
            })
        else:
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
                'order_user_name': order_obj.order_user_name,
                'phone_number': order_obj.phone_number,
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
            'boxes': resources,
            'carwash_start_time': carwash_start_time,
            'carwash_end_time': carwash_end_time,
            'date_today': date_today,
            'now_iso': now_iso,
            'scrollToTime': now_format,
            'carwash_id': carwash_id,
        }
        return context

    set_prices = get_price_list(carwash_obj.Price)
    context = {
        'calendar': {
            'orders': events,
            'boxes': resources,
            'carwash_start_time': carwash_start_time,
            'carwash_end_time': carwash_end_time,
            'date_today': date_today,
            'now_iso': now_iso,
            'scrollToTime': now_format,
            'carwash_id': carwash_id,
        },
        # 'set_prices': set_prices,
        'carwash': carwash_obj,
        'enum_list': list(CategoryAuto),
        'category': Catergory,
        'box': get_amount_boxes(carwash_obj),
        'basket': None

    }
    return render_template('schedule/view_schedule.html', context=context)


def get_order_basket_arr(data):
    basket_arr = []
    for key, value in data.items():
        if 'amount_' in key:
            price_id = key.split('_')[1]
            basket_arr.append(basketItem(id=price_id, amount=int(data[key]), price=int(data['basecost_' + price_id])))
    return basket_arr


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
    try:
        order_user_name = data['order_user_name']
        phone_number = data['phone_number']
        box = request.form['box']
        country_region_number = request.form['country_region_number']
        car_brand = request.form['car_brand']
        car_model = request.form['car_model']
        category = request.form['category']
        sum_of_basket = request.form['total-hidden']
    except Exception:
        error_message = "Заполните все необходимые поля!"
        return abort(Response(error_message, 400))
    order_basket = json.loads(json.dumps(get_order_basket_arr(data), default=lambda x: x.__dict__))
    # print('order_basket: ', order_basket)
    # print('order_basket: ', json.loads(json.dumps(order_basket, default=lambda x: x.__dict__)))

    contract_id = 'OWN'
    Status = 'LocalOrder'
    date_created = datetime.now().isoformat()
    date_start = datetime.strptime(request.form['date'] + ' ' + request.form['time_start'],
                                   "%Y-%m-%d %H:%M").isoformat()
    date_end = datetime.strptime(request.form['date'] + ' ' + request.form['time_end'],
                                 "%Y-%m-%d %H:%M").isoformat()

    order = {
        '_id': order_id,
        'order_basket': order_basket,
        'order_user_name': order_user_name,
        'phone_number': phone_number,
        'CarWashId': carwash_id,
        'BoxNumber': box,
        'CarNumber': country_region_number,
        'CarModel': car_model,
        'CarBrand': car_brand,
        'Category': category,
        'ContractId': contract_id,
        'Sum': sum_of_basket,
        'Status': Status,
        'DateCreate': date_created,
        'DateStart': date_start,
        'DateEnd': date_end,
        'network_id': network_id,
    }

    print('Writing into DB')
    print(order)
    database.col_orders.insert_one(order)

    # формирование ответа
    return jsonify(success=True)


def edit_carwash_order(request, carwash_id):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print(data, carwash_id)
    print('\n################################################################\n')

    id_order = {'_id': request.form['order_id']}
    print('id_order: ', request.form['order_id'])
    print('TIME_PARAMS: \n', request.form['date'] + ' ' + request.form['time_start'] + ' ' + request.form['time_end'])
    set_fields = {'$set': {
        'order_basket': json.loads(json.dumps(get_order_basket_arr(data), default=lambda x: x.__dict__)),
        'order_user_name': data['order_user_name'],
        'phone_number': data['phone_number'],
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


def count_total_price(basket):
    total_price = 0
    for basket_item in basket.values():
        total_price += basket_item.pre_total_price
    return total_price


def is_in_(search, price):
    search = to_rus(search)
    if search in price.name:
        return True
    if search in price.description:
        return True
    if search in str(price.name).lower():
        return True
    if search in str(price.name).upper():
        return True
    search = to_eng(search)
    if search in price.name:
        return True
    if search in price.description:
        return True
    if search in str(price.name).lower():
        return True
    if search in str(price.name).upper():
        return True


def backend_search_prices(request, carwash_id):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print(data, carwash_id)
    print('\n################################################################\n')

    selected_category = request.form['category'] if 'category' in request.form else None
    if selected_category is None:
        return abort(404)
    search = request.form['search-field']

    print('selected_category: ', selected_category)
    print('search: ', search)
    print('carwash_id:', carwash_id)
    carwash_obj = get_carwash_obj(carwash_id)

    print('price_id: ', carwash_obj.Price)
    price_list = get_price_list(carwash_obj.Price)
    print('price_list: ', price_list)

    res_of_search = []
    for price in price_list:
        if is_in_(search, price):
            res_of_search.append(price)

    # формирование ответа
    # response = {'status': 'success'}
    context = {
        'set_prices': res_of_search,
    }
    return render_template('schedule/table_of_results.html', context=context)


def get_price(price_id):
    price_obj = database.col_prices.find_one({'_id': price_id})  # dict
    data = json.loads(json_util.dumps(price_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print('price_obj: ', price_obj)
    return price_obj


def backend_add_price_to_order(request, carwash_id, price_id):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print('data: ', data)
    print('carwash_id: ', carwash_id)
    print('price_id: ', price_id)
    print('\n################################################################\n')

    for key, value in data.items():
        if 'amount_' in key:
            print('table is not empty')
            if price_id == key.split('_')[1]:
                abort(404)
            else:
                pass
        else:
            print('table empty')
    # добавление в таблицу заказа еще одного НОВОГО тарифа
    print(data, price_id)
    selected_category = data['category']
    price_obj = get_price(price_id)
    for obj in price_obj.categoryPrice:
        if obj.category == selected_category:
            price_obj.categoryPrice = obj
    pretotal_price = price_obj.categoryPrice.sum
    setattr(price_obj, 'amount', 1)
    setattr(price_obj, 'pretotal_price', pretotal_price)
    print('pretotal_price: ', pretotal_price)
    arr_of_price = [price_obj]

    context = {
        'set_prices': arr_of_price,
    }
    return render_template('schedule/table_prices.html', context=context)


def backend_calculate_total(request, carwash_id):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print('data: ', data)
    print('carwash_id: ', carwash_id)
    print('\n################################################################\n')
    total = 0
    for key, value in data.items():
        if 'amount_' in key:
            price_id = key.split("_")[1]
            print(f'Ценник - {price_id} -> {data[key]}шт.')

            total += int(data[key]) * int(data['basecost_' + price_id])
    return {'total': total}


# --------------------------------
def backend_remove_price_from_order(request, carwash_id, price_id):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print('data: ', data)
    print('carwash_id: ', carwash_id)
    print('price_id: ', price_id)
    print('\n################################################################\n')
    set_prices = []
    for key, value in data.items():
        # amount_5de6e8b26bd04c53996bacbe363a5a1e
        if 'amount_' in key:
            if price_id.split('_')[1] == key.split('_')[1]:
                pass
            else:
                price_obj = get_price(key.split('_')[1])
                for obj in price_obj.categoryPrice:
                    if obj.category == data['category']:
                        price_obj.categoryPrice = obj
                pretotal_price = int(price_obj.categoryPrice.sum) * int(data[key])
                setattr(price_obj, 'amount', data[key])
                setattr(price_obj, 'pretotal_price', pretotal_price)
                print('pretotal_price: ', pretotal_price)
                set_prices.append(price_obj)
    context = {
        'set_prices': set_prices
    }
    return render_template('schedule/table_prices.html', context=context)


def backend_increment_price_in_order(request, carwash_id, price_id):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print('data: ', data)
    print('carwash_id: ', carwash_id)
    print('price_id: ', price_id)
    print('\n################################################################\n')
    set_prices = []
    for key, value in data.items():
        # amount_5de6e8b26bd04c53996bacbe363a5a1e
        if 'amount_' in key:
            if price_id.split('_')[1] == key.split('_')[1]:
                price_obj = get_price(key.split('_')[1])
                for obj in price_obj.categoryPrice:
                    if obj.category == data['category']:
                        price_obj.categoryPrice = obj
                pretotal_price = int(price_obj.categoryPrice.sum) * (int(data[key]) + 1)
                setattr(price_obj, 'amount', int(data[key]) + 1)
                setattr(price_obj, 'pretotal_price', pretotal_price)
                print('pretotal_price: ', pretotal_price)
                set_prices.append(price_obj)
            else:
                price_obj = get_price(key.split('_')[1])
                for obj in price_obj.categoryPrice:
                    if obj.category == data['category']:
                        price_obj.categoryPrice = obj
                pretotal_price = int(price_obj.categoryPrice.sum) * int(data[key])
                setattr(price_obj, 'amount', data[key])
                setattr(price_obj, 'pretotal_price', pretotal_price)
                print('pretotal_price: ', pretotal_price)
                set_prices.append(price_obj)
    context = {
        'set_prices': set_prices
    }
    return render_template('schedule/table_prices.html', context=context)


def backend_decrement_price_in_order(request, carwash_id, price_id):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print('data: ', data)
    print('carwash_id: ', carwash_id)
    print('price_id: ', price_id)
    print('\n################################################################\n')

    set_prices = []
    for key, value in data.items():
        # amount_5de6e8b26bd04c53996bacbe363a5a1e
        if 'amount_' in key:
            if price_id.split('_')[1] == key.split('_')[1]:
                price_obj = get_price(key.split('_')[1])
                for obj in price_obj.categoryPrice:
                    if obj.category == data['category']:
                        price_obj.categoryPrice = obj
                if int(data[key]) < 2:
                    backend_remove_price_from_order(request, carwash_id, price_id)  # если кол-во меньше 2 - удалить
                else:
                    pretotal_price = int(price_obj.categoryPrice.sum) * (int(data[key]) - 1)
                    setattr(price_obj, 'amount', int(data[key]) - 1)
                    setattr(price_obj, 'pretotal_price', pretotal_price)
                    print('pretotal_price: ', pretotal_price)
                    set_prices.append(price_obj)
            else:
                price_obj = get_price(key.split('_')[1])
                for obj in price_obj.categoryPrice:
                    if obj.category == data['category']:
                        price_obj.categoryPrice = obj
                pretotal_price = int(price_obj.categoryPrice.sum) * int(data[key])
                setattr(price_obj, 'amount', data[key])
                setattr(price_obj, 'pretotal_price', pretotal_price)
                print('pretotal_price: ', pretotal_price)
                set_prices.append(price_obj)
    context = {
        'set_prices': set_prices
    }
    return render_template('schedule/table_prices.html', context=context)


def get_order(order_id):
    order_obj = database.col_orders.find_one({'_id': order_id})  # dict
    data = json.loads(json_util.dumps(order_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print('order_obj: ', order_obj)
    return order_obj


def backend_get_order_basket(request, carwash_id):
    print('\n########################DATA####################################\n')
    data = request.form.to_dict()
    print('data: ', data)
    print('carwash_id: ', carwash_id)
    print('\n################################################################\n')
    set_prices = []
    order_obj = get_order(data['order_id'])
    if order_obj is None:
        return {}
    for price in order_obj.order_basket:
        price_obj = get_price(price._id)
        for obj in price_obj.categoryPrice:
            if obj.category == data['category']:
                price_obj.categoryPrice = obj
        pretotal_price = int(price.amount) * int(price.price)
        setattr(price_obj, 'amount', price.amount)
        setattr(price_obj, 'pretotal_price', pretotal_price)
        set_prices.append(price_obj)
    context = {
        'set_prices': set_prices
    }
    return render_template('schedule/table_prices.html', context=context)
