import json
import os
import traceback
from types import SimpleNamespace

from bson import json_util
from flask import Blueprint, request, Response, render_template, g, session, redirect, url_for

from .backend import get_statistics
from ..configuration.config import Config

from flask_login import current_user

from ..db import database
from ..main import oauth_via_yandex

statistics_bp = Blueprint(
    'statistics_blueprint', __name__,
)


@statistics_bp.before_request
def load_user():
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    g.user_inf = user_inf
    print('g.user_inf: ', g.user_inf)
    user = database.col_users.find_one({'_id': user_inf['id']})
    g.user_db = user
    print('g.user_db: :', g.user_db)


@statistics_bp.route('/statistics/', methods=['POST', 'GET'])
def statistics():
    return get_statistics(g)


@statistics_bp.route('/test/', methods=['POST', 'GET'])
def test():
    return render_template('testing/test_header.html')
