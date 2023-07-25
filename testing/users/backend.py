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


def list_workers():
    all_users = database.col_users.find({})
    user_list = []
    for i in all_users:
        user_obj = json.dumps(i, default=default)
        user_obj = json.loads(user_obj, object_hook=lambda d: SimpleNamespace(**d))
        user_list.append(user_obj)
        print('\nuser_obj: ', user_obj, '\n')
    print(user_list)
    context = {
        'user_list': user_list,
    }
    return render_template('users/users_list.html', context=context)

