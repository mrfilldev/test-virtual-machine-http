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

        context = {}
        print('context: ', context)
        return redirect(url_for('users_blueprint.users_list'))

    all_carwashes = database.col_carwashes.find({'network_id': g_user_flask.user_db['networks'][0]})
    carwashes = []
    for carwash in all_carwashes:
        carwash_obj = get_obj(carwash)
        carwashes.append(carwash_obj)

    print('carwashes: ', carwashes)
    context = {
        'user': user_obj,
        'carwashes': carwashes,
    }

    return render_template('users/user_detail.html', context=context)
