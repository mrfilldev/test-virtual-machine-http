import json
import uuid
from types import SimpleNamespace

from bson import json_util
from flask import render_template, session, redirect, url_for

from ..db import database
from ..db.models import User, UserRole
from ..main import oauth_via_yandex


def users_list_view():
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    all_users = database.col_users.find({})
    users_list = []
    count_users = 0
    for count_users, i in enumerate(list(all_users)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        user_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
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
        new_value = request.form['role']
        set_command = {"$set": {"role": new_value}}
        old_user = {'_id': str(user_id)}
        new_user = database.col_users.update_one(old_user, set_command)
        print('new_user', new_user)

    user_obj = database.col_users.find_one({'_id': str(user_id)})  # dict
    print(user_obj)

    data = json.loads(json_util.dumps(user_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    user_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print(user_obj)

    for i in UserRole:
        print(i.name, i.value)

    context = {
        'user': user_obj,
        'UserRole': UserRole
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
