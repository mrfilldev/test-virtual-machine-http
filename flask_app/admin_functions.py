import json
from types import SimpleNamespace

from bson import json_util
from flask import render_template

from flask_app import oauth_via_yandex
from config.config import Config

users = Config.col_users


def check_root(session):
    """
    1. получить по токену сессии имя uid
    2. найти пользователя с uid в монге
    3. проверить его уровень допуска
    ________________________________________________________________

    :return:

    вернуть объект || вернуть цифру уровня допуска
    """
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    user_id = user_inf['id']
    user = users.find_one({'id': user_id})

    if user['access_level'] == 'admin':
        return 'admin'
    else:
        return 'user'


def admin_main(request, session):
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    inf_list = []
    for k in user_inf:
        inf_list.append(f"{k} -> {user_inf[k]} \n")
    print(user_inf)

    status = 'admin'
    context = {
        'user': user_inf,
        'inf_list': inf_list,
        'status': status

    }
    return render_template('admin_zone/admin_main.html', context=context)
