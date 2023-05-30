import json
import os
import traceback
from datetime import date
import random
from types import SimpleNamespace

from bson import json_util
from dateutil import parser
from flask import Blueprint, request, Response, render_template, g, session, redirect, url_for

from flask_login import current_user

from .backend import show_list_sets_prices, set_create, set_detail, create_price, get_info_about_price
from ..configuration.config import Config
from ..db import database
from ..main import oauth_via_yandex

prices_bp = Blueprint(
    'prices_blueprint', __name__,
)


@prices_bp.before_request
def load_user():
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    g.user_inf = user_inf
    print('g.user_inf: ', g.user_inf)
    user = database.col_users.find_one({'_id': user_inf['id']})
    g.user_db = user
    print('g.user_db: :', g.user_db)


@prices_bp.route('/list_sets_prices/', methods=['GET'])
def list_sets_prices():
    return show_list_sets_prices()


@prices_bp.route('/new_set/', methods=['POST', 'GET'])
def new_set():
    return set_create(request)


@prices_bp.route('/set_detail/<string:set_id>', methods=['POST', 'GET'])
def detail_set(set_id):
    return set_detail(request, set_id)


@prices_bp.route('/new_price/<string:set_id>', methods=['POST', 'GET'])
def new_price(set_id):
    return create_price(request, set_id)

@prices_bp.route('/info_price/<string:price_id>', methods=['POST', 'GET'])
def info_price(price_id=''):
    return get_info_about_price(price_id)


@prices_bp.app_template_filter()
def smthing(smthing):
    match smthing:
        case 'Compact':
            pass
        case _:
            pass
