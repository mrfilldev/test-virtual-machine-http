import json
import os
import traceback
from datetime import date
from types import SimpleNamespace

from bson import json_util
from dateutil import parser
from flask import Blueprint, request, Response, render_template, g, session, redirect, url_for


from flask_login import current_user

from .view_schedule import view_schedule
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


@schedule_bp.route('/schedule', methods=['POST', 'GET'])
def schedule():
    return view_schedule(g)


@schedule_bp.app_template_filter()
def format_datetime_hour_minute(value):
    if isinstance(value, date):
        value = value.strftime("%H:%M")
    else:
        value = parser.parse(value)
        value = value.strftime("%H:%M")
    return value