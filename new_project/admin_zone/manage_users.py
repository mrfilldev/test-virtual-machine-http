import json
from types import SimpleNamespace

from bson import json_util
from flask import render_template

from ..db import database
from ..main import oauth_via_yandex


def test_view(session):
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