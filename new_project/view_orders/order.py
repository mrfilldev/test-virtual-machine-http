import json
import os
import traceback
from types import SimpleNamespace

from bson import json_util
from flask import Blueprint, request, Response, render_template, g, session, redirect, url_for

from .work_with_orders import list_orders
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


@order_bp.route('/orders_list', methods=['POST', 'GET'])
def orders_list():
    return list_orders(g)
