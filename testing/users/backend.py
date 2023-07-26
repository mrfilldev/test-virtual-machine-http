import json
import uuid
import datetime

from types import SimpleNamespace

from bson import json_util
from flask import render_template, url_for, redirect, jsonify, abort, request

from ..db import database
from ..db.models import Boxes, BoxStatus, PricesCarWash, Point, Types, Carwash, CategoryAuto, Prices


def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()


def get_obj(obj):
    obj = json.dumps(obj, default=default)
    obj = json.loads(obj, object_hook=lambda d: SimpleNamespace(**d))
    return obj


def list_workers(g_user_flask):
    all_users = database.col_users.find({})
    workers_list = []
    for i in all_users:
        user_obj = get_obj(i)
        if user_obj.role == 'network_worker' and user_obj.networks[0] == g_user_flask.user_db['networks'][0]:
            workers_list.append(user_obj)
        print('\nuser_obj: ', user_obj, '\n')
    print(workers_list)
    context = {
        'user_list': workers_list,
    }
    return render_template('users/users_list.html', context=context)


def user_detail(g_user_flask, user_id):
    user = database.col_users.find_one({'_id': str(user_id)})  # dict
    user_obj = get_obj(user)
    print('\nuser_obj: ', user_obj, '\n')
    if request.method == 'POST':
        print('\n################################################################\n')
        dict_of_form = request.form.to_dict(flat=False)
        print(dict_of_form)
        print('################################################################\n')
        for k, v in dict_of_form.items():
            print(k, '-> ', v)
        print('\n################################################################\n')
        try:
            user = {'_id': user_id}
            print('user: ', user)
            set_fields = {'$set': {
                'PinnedCarwashId': request.form['PinnedCarwashId'],
                'network': form['name'],
                'Address': form['address'],
                'Location': {'lat': form['lat'], 'lon': form['lon']},
                'Type': Types.SelfService.name,
                'Boxes': new_boxes_list_of_dict,
                'Price': request.form['set_of_price'],
                # json.loads(json.dumps(create_prices(request, dict_of_form, update=True, carwash_id=carwash_id),default=lambda x: x.__dict__)),
                'IsCarwash': is_hand_carwash,
                'IsWheelStation': is_wheel_station,
                'IsDetaling': is_detaling,
            }}
            new_carwash = database.col_carwashes.update_one(old_carwash, set_fields)
        except Exception as e:
            print("Error updating")

        context = {}
        print('context: ', context)
        return redirect(url_for('users_blueprint.users_list'))

    all_carwashes = database.col_carwashes.find({'network_id': g_user_flask.user_db['networks'][0]})
    carwashes = []
    for carwash in all_carwashes:
        carwash_obj = get_obj(carwash)
        carwashes.append(carwash_obj)
    print('carwashes: ', carwashes)

    all_networks = database.col_networks.find({})
    networks = []
    for network in all_networks:
        network_obj = get_obj(network)
        if network_obj._id in g_user_flask.user_db['networks']:
            networks.append(network_obj)

    context = {
        'user': user_obj,
        'carwashes': carwashes,
        'networks': networks,
    }

    return render_template('users/user_detail.html', context=context)
