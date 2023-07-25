import json
import os
import traceback
from types import SimpleNamespace

from bson import json_util
from flask import Blueprint, request, Response, render_template, g, session, redirect, url_for

from .backend import list_workers, user_detail
from ..configuration.config import Config

from flask_login import current_user

from ..db import database
from ..db.models import BoxAmountStatus
from ..main import oauth_via_yandex

users_bp = Blueprint(
    'users_blueprint', __name__,
)


@users_bp.before_request
def load_user():
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    g.user_inf = user_inf
    print('g.user_inf: ', g.user_inf)
    user = database.col_users.find_one({'_id': user_inf['id']})
    g.user_db = user
    print('g.user_db: :', g.user_db)


@users_bp.errorhandler(500)
def page_not_found(e):
    return render_template("error_page/500.html"), 500


@users_bp.route('/users_list', methods=['POST', 'GET'])
def users_list():
    return list_workers(g)


@users_bp.route('/user/<string:user_id>', methods=['POST', 'GET'])
def user(user_id):
    return user_detail(g, user_id)
