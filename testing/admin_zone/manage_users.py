import json
import uuid
from types import SimpleNamespace

from bson import json_util
from flask import render_template, session, redirect, url_for

from ..db import database
from ..db.models import User, UserRole
from ..main import oauth_via_yandex

import datetime
import json


def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()


def users_list_view():
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    all_users = database.col_users.find({})
    users_list = []
    count_users = 0
    for count_users, i in enumerate(list(all_users)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        user_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

        test_obj = json.dumps(i, default=default)
        order_obj = json.loads(test_obj, object_hook=lambda d: SimpleNamespace(**d))
        print('\norder_obj: ', order_obj, '\n')

        print(user_obj)
        users_list.append(user_obj)
    print(users_list)
    inf_list = []
    for k in user_inf:
        inf_list.append(f"{k} -> {user_inf[k]} \n")
    print(user_inf)
    context = {
        'user': user_inf,
        'inf_list': inf_list,
        'users_list': users_list,
        'count_users': count_users,
    }
    return render_template(
        'admin/test.html',
        context=context
    )


def user_detail(request, user_id):
    if request.method == 'POST':
        user_obj = database.col_users.find_one({'_id': str(user_id)})  # dict
        data = json.loads(json_util.dumps(user_obj))
        data = json.dumps(data, default=lambda x: x.__dict__)
        user_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
        print('user_obj: ', user_obj)
        empty_arr = []
        empty_arr.append(request.form['network'])
        print('empty_arr: ', empty_arr)

        set_fields = {'$set': {
            "role": request.form['role'],
            "networks": empty_arr,
        }}
        database.col_users.update_one({'_id': user_obj._id}, set_fields)

        context = {
            'user': user_obj,
            'UserRole': UserRole,
            'networks': empty_arr,
        }
        print('context: ', context)
        # return redirect(url_for('admin_blueprint.admin_user_detail', user_id=user_obj._id))

    user_obj = database.col_users.find_one({'_id': str(user_id)})  # dict
    print(user_obj)

    data = json.loads(json_util.dumps(user_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    user_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print(user_obj)

    for i in UserRole:
        print(i.name, i.value)

    network_obj = database.col_networks.find({})  # dict
    data = json.loads(json_util.dumps(network_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    network_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print(network_obj)

    context = {
        'user': user_obj,
        'UserRole': UserRole,
        'networks': network_obj,
    }
    return render_template(
        'admin/user_detail.html',
        context=context
    )


def add_user(request):
    print('\n################################################################\n')
    form = request.form

    id = uuid.uuid4().hex

    new_user = User(Id=id, email=form['email'], role=form.role)

    new_user_json = json.dumps(new_user, default=lambda x: x.__dict__)
    new_user_dict = json.loads(new_user_json)
    new_user_dict['_id'] = new_user_dict.pop('Id')

    database.col_users.insert_one(new_user_dict)
    print("User inserted successfully")


def delete_user(user_id):
    database.col_users.delete_one({'_id': user_id})
    print(f'User {user_id} deleted successfully')
    return redirect(url_for('admin_blueprint.admin_users'))
