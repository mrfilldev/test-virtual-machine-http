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

from .view_schedule import create_carwash_order, view_schedule_of_certain_carwash, edit_carwash_order, \
    backend_search_prices, \
    backend_add_price_to_order, backend_calculate_total, backend_remove_price_from_order, \
    backend_increment_price_in_order, backend_decrement_price_in_order, backend_get_order_basket
from ..configuration.config import Config
from ..db import database
from ..main import oauth_via_yandex

schedule_bp = Blueprint(
    'schedule_blueprint', __name__,
)


@schedule_bp.before_request
def load_user():
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    g.user_inf = user_inf
    print('g.user_inf: ', g.user_inf)
    user = database.col_users.find_one({'_id': user_inf['id']})
    g.user_db = user
    print('g.user_db: :', g.user_db)


# @schedule_bp.route('/schedule', methods=['GET'])
# def schedule():
#     return view_schedule(g)


@schedule_bp.route('/schedule_certain_carwash/<string:carwash_id>', methods=['GET'])
def schedule_certain_carwash(carwash_id):
    return view_schedule_of_certain_carwash(request, carwash_id, g)


@schedule_bp.route('/create_order_carwash/<string:carwash_id>', methods=['POST'])
def create_order_carwash(carwash_id):
    return create_carwash_order(request, carwash_id)


@schedule_bp.route('/edit_order_carwash/<string:carwash_id>', methods=['POST'])
def edit_order_carwash(carwash_id):
    return edit_carwash_order(request, carwash_id)



@schedule_bp.route('/search_prices/<string:carwash_id>', methods=['POST'])
def search_prices(carwash_id):
    return backend_search_prices(request, carwash_id)


@schedule_bp.route('/add_price_to_order/<string:carwash_id>', methods=['POST'])
@schedule_bp.route('/add_price_to_order/<string:carwash_id>&<string:price_id>', methods=['POST'])
def add_price_to_order(carwash_id, price_id):
    return backend_add_price_to_order(request, carwash_id, price_id)


@schedule_bp.route('/calculate_total/<string:carwash_id>', methods=['POST'])
def calculate_total(carwash_id):
    return backend_calculate_total(request, carwash_id)


@schedule_bp.route('/remove_price_from_order/<string:carwash_id>', methods=['POST'])
@schedule_bp.route('/remove_price_from_order/<string:carwash_id>&<string:price_id>', methods=['POST'])
def remove_price_from_order(carwash_id, price_id):
    return backend_remove_price_from_order(request, carwash_id, price_id)


@schedule_bp.route('/increment_price_in_order/<string:carwash_id>', methods=['POST'])
@schedule_bp.route('/increment_price_in_order/<string:carwash_id>&<string:price_id>', methods=['POST'])
def increment_price_in_order(carwash_id, price_id):
    return backend_increment_price_in_order(request, carwash_id, price_id)


@schedule_bp.route('/decrement_price_in_order/<string:carwash_id>', methods=['POST'])
@schedule_bp.route('/decrement_price_in_order/<string:carwash_id>&<string:price_id>', methods=['POST'])
def decrement_price_in_order(carwash_id, price_id):
    return backend_decrement_price_in_order(request, carwash_id, price_id)


@schedule_bp.route('/get_order_basket/<string:carwash_id>', methods=['POST'])
def get_order_basket(carwash_id):
    return backend_get_order_basket(request, carwash_id)


@schedule_bp.app_template_filter()
def format_datetime_hour_minute(value):
    if isinstance(value, date):
        value = value.strftime("%H:%M")
    else:
        value = parser.parse(value)
        value = value.strftime("%H:%M")
    return value


@schedule_bp.app_template_filter()
def random_value(list_of_strings: list):
    return random.choice(list_of_strings)
