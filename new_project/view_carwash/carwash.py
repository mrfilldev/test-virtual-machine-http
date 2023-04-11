import json
import os
import traceback
from types import SimpleNamespace

from bson import json_util
from flask import Blueprint, request, Response, render_template, g, session, redirect, url_for

from .manage_carwashes import create_carwash_obj, carwash_detail, carwash_delete, list_carwashes
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
    return list_carwashes(g)


@carwash_bp.route('/create_carwash', methods=['POST', 'GET'])
def create_carwash():
    create_carwash_obj(request, g)



@carwash_bp.route('/create_carwash/<string:carwash_id>', methods=['POST', 'GET'])
def owner_carwash_detail(carwash_id):
    carwash_detail(request, carwash_id)

@carwash_bp.route('/delete_carwash/<string:carwash_id>', methods=['POST', 'GET'])
def delete_carwash(carwash_id):
    carwash_delete(carwash_id)

