import json
import os
import traceback
from types import SimpleNamespace

from bson import json_util
from flask import Blueprint, request, Response, render_template, g, session, redirect, url_for

from .work_with_orders import list_orders, owner_order_detail, accept_order, complete_order, cancel_order
from ..configuration.config import Config

from flask_login import current_user

from ..db import database
from ..main import oauth_via_yandex

order_bp = Blueprint(
    'order_blueprint', __name__,
)


@order_bp.before_request
def load_user():
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    g.user_inf = user_inf
    print('g.user_inf: ', g.user_inf)
    user = database.col_users.find_one({'_id': user_inf['id']})
    g.user_db = user
    print('g.user_db: :', g.user_db)


@order_bp.route('/orders_list/', methods=['POST', 'GET'])
@order_bp.route('/orders_list/<string:skip>-<string:limit>', methods=['POST', 'GET'])
def orders_list(skip=0, limit=25):
    return list_orders(g, int(skip), int(limit))


@order_bp.route('/order_detail/<string:order_id>', methods=['POST', 'GET'])
def order_detail(order_id):
    return owner_order_detail(order_id)


@order_bp.route('/order_accept/<string:order_id>', methods=['POST', 'GET'])
def order_accept(order_id):
    accept_order(order_id)
    return redirect(url_for('order_blueprint.orders_list'))


@order_bp.route('/order_complete/<string:order_id>', methods=['POST', 'GET'])
def order_complete(order_id):
    complete_order(order_id)
    return redirect(url_for('order_blueprint.orders_list'))


@order_bp.route('/order_cancel/<string:order_id>', methods=['POST', 'GET'])
def order_cancel(order_id):
    cancel_order(order_id)
    return redirect(url_for('order_blueprint.orders_list'))
