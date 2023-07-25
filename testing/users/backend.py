import json
import uuid
import datetime

from types import SimpleNamespace

from bson import json_util
from flask import render_template, url_for, redirect, jsonify, abort

from ..db import database
from ..db.models import Boxes, BoxStatus, PricesCarWash, Point, Types, Carwash, CategoryAuto, Prices


def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()


def list_workers(g_user_flask):
    all_users = database.col_users.find({})
    workers_list = []
    for i in all_users:
        user_obj = json.dumps(i, default=default)
        user_obj = json.loads(user_obj, object_hook=lambda d: SimpleNamespace(**d))

        if user_obj.role == 'network_worker' and user_obj.networks[0] == g_user_flask.user_db['networks'][0]:
            workers_list.append(user_obj)
        print('\nuser_obj: ', user_obj, '\n')
    print(workers_list)
    context = {
        'user_list': workers_list,
    }
    return render_template('users/users_list.html', context=context)

