import json
import os
import traceback
from types import SimpleNamespace

from bson import json_util
from flask import Blueprint, request, Response, render_template, g, session, redirect, url_for

from .manage_carwashes import create_carwash_obj, carwash_detail, delete_carwash
from ..configuration.config import Config

from flask_login import current_user

from ..db import database
from ..main import oauth_via_yandex

carwash_bp = Blueprint(
    'carwash_blueprint', __name__,
)


@carwash_bp.before_request
def load_user():
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    g.user_inf = user_inf
    print('g.user_inf: ', g.user_inf)
    user = database.col_users.find_one({'_id': user_inf['id']})
    g.user_db = user
    print('g.user_db: :', g.user_db)


@carwash_bp.route('/carwash_list', methods=['POST', 'GET'])
def carwashes_list():
    id_user = g.user_db['_id']
    if 'networks' in g.user_db:
        network = g.user_db['networks'][0]
        all_carwashes = database.col_carwashes.find({'network_id': network})
        print('network:', network)
        network = database.col_networks.find({'_id': network})
        data = json.loads(json_util.dumps(network))
        data = json.dumps(data, default=lambda x: x.__dict__)
        network_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))[0]  # SimpleNamespace
        print('network_obj:', network_obj)
    else:
        all_carwashes = database.col_carwashes.find({})
        network_obj = None
    carwashes_list = []
    count_carwashes = 0

    for count_carwashes, i in enumerate(list(all_carwashes)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        carwashes_list.append(carwash_obj)
        print(carwash_obj)
    print(carwashes_list)

    context = {
        'carwashes_list': carwashes_list,
        'count_carwashes': count_carwashes,
        'network_obj': network_obj,
    }
    return render_template('view_carwash/carwash_list.html', context=context)


@carwash_bp.route('/create_carwash', methods=['POST', 'GET'])
def create_carwash():
    create_carwash_obj(request, g)



@carwash_bp.route('/create_carwash/<string:carwash_id>', methods=['POST', 'GET'])
def owner_carwash_detail(carwash_id):
    carwash_detail(request, carwash_id)

@carwash_bp.route('/delete_carwash/<string:carwash_id>', methods=['POST', 'GET'])
def user_carwash_detail(carwash_id):
    delete_carwash(carwash_id)

