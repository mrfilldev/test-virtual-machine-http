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

from .backend import view_boxes
from ..configuration.config import Config
from ..db import database
from ..main import oauth_via_yandex

box_panel_bp = Blueprint(
    'box_panel_blueprint', __name__,
)


@box_panel_bp.before_request
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


@box_panel_bp.route('/operation_panel_boxes/<string:carwash_id>', methods=['GET'])
def box_panel(carwash_id):
    return view_boxes(request, carwash_id, g)


@box_panel_bp.app_template_filter()
def status_to_rus(status):
    match status:
        case 'Free':
            return 'Свободен'
        case 'Busy':
            return 'Занят'
        case 'Unavailable':
            return 'Недоступен'
        case _:
            return status
