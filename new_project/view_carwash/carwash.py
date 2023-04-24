import json
import os
import traceback
from types import SimpleNamespace

from bson import json_util
from flask import Blueprint, request, Response, render_template, g, session, redirect, url_for
from markupsafe import Markup

from .work_with_carwashes import create_carwash_obj, carwash_detail, carwash_delete, list_carwashes
from ..configuration.config import Config

from flask_login import current_user

from ..db import database
from ..db.models import BoxAmountStatus
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
    return create_carwash_obj(request, g)


@carwash_bp.route('/carwash_detail/<string:carwash_id>', methods=['POST', 'GET'])
def owner_carwash_detail(carwash_id):
    return carwash_detail(g, request, carwash_id)


@carwash_bp.route('/delete_carwash/<string:carwash_id>', methods=['POST', 'GET'])
def delete_carwash(carwash_id):
    return carwash_delete(carwash_id)


@carwash_bp.app_template_filter()
def format_pretty_boxes(boxes):
    print("\nboxes: %s" % boxes)
    free = 0
    busy = 0
    unavailable = 0
    for i in range(len(boxes)):
        print(boxes[i])
        if boxes[i].status == 'Free':
            free += 1
        elif boxes[i].status == 'Busy':
            busy += 1
        elif boxes[i].status == 'Unavailable':
            unavailable += 1
    print(" free: %s" % free)
    print(" busy: %s" % busy)
    print(" unavailable: %s" % unavailable)
    boxes_status = BoxAmountStatus(free, busy, unavailable)
    return boxes_status


@carwash_bp.app_template_filter()
def enable_rus(enable):
    if enable:
        return 'Активна'
    else:
        return 'Не активна'


@carwash_bp.app_template_filter()
def type_rus(type_of_carwash):
    if type_of_carwash == 'SelfServiceFixPrice':
        return 'автомойка самообслуживания Фикс-Цена'
    elif type_of_carwash == 'SelfService':
        return 'автомойка самообслуживания'
    elif type_of_carwash == 'Contactless':
        return 'безконтактная'
    elif type_of_carwash == 'Manual':
        return 'ручная мойка'
    elif type_of_carwash == 'Portal':
        return 'портальная'
    elif type_of_carwash == 'Tunnel':
        return 'тунельная'
    elif type_of_carwash == 'Dry':
        return 'сухая'
    else:
        return type_of_carwash
