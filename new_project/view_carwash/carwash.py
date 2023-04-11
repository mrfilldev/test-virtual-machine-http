import json
import os
import traceback
from types import SimpleNamespace

from bson import json_util
from flask import Blueprint, request, Response, render_template, g, session, redirect, url_for
from ..configuration.config import Config

from flask_login import current_user

from ..db import database
from ..main import oauth_via_yandex

carwash_bp = Blueprint(
    'carwash_blueprint', __name__,
)

@carwash_bp.route('/carwash_list')
def carwash_list():
    id_user = g.user_db['_id']
    network = g.user_db['networks'][0]

    carwashes_list = []
    all_carwashes = database.col_carwashes.find({'network_id': network})
    count_carwashes = 0

    for count_carwashes, i in enumerate(list(all_carwashes)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        carwashes_list.append(carwash_obj)
        print(carwash_obj)
    context = {
        'carwashes_list': carwashes_list,
        'count_carwashes': count_carwashes,
    }

    context = {

    }
    render_template('view_carwash/carwash_list.html', context=context)
