import json
from types import SimpleNamespace

from bson import json_util
from flask import session, render_template, redirect, url_for
from functools import wraps

from flask_login import LoginManager

from flask_app import oauth_via_yandex
from config.config import Config
from flask_app.urls import login_manager

owners = Config.col_owners
users = Config.col_users


def get_infor():
    # user = dict(session).get('ya-token', None)
    # user_yan_inf = oauth_via_yandex.get_user(session['ya-token'])
    current_user.role == 'admin'
    # user = owners.find_one({'_id': user_yan_inf['id']})
    # print(user)
    # data = json.loads(json_util.dumps(user))
    # data = json.dumps(data, default=lambda x: x.__dict__)
    # user = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    # print(user)
    return user


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('ya-token', None)
        if user:
            return f(*args, **kwargs)
        # выброс на авторизацию
        return redirect(url_for('oauth'))

    return decorated_function


def admin_status_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_infor()
        if user.access_level == 'admin':
            return f(*args, **kwargs)
        # выброс на авторизацию
        return redirect(url_for('profile'))

    return decorated_function


def owner_status_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_infor()
        if user.access_level == 'Владелец сети' or user.access_level == 'admin':
            return f(*args, **kwargs)
        # выброс на авторизацию
        return redirect(url_for('profile'))

    return decorated_function


def carwasher_status_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_infor()
        if user.access_level == 'Сотрудник мойки':
            return f(*args, **kwargs)
        # выброс на авторизацию
        return redirect(url_for('profile'))

    return decorated_function


def user_loader(f):
    @wraps(f)
    def decorated_function():
        return oauth_via_yandex.get_user(session['ya-token'])
    return decorated_function
