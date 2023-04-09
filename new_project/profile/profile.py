import os
import traceback
from flask import Blueprint, request, Response, render_template, g, session
from ..configuration.config import Config

from flask_login import current_user

from ..db import database
from ..main import oauth_via_yandex

profile_bp = Blueprint(
    'profile_blueprint', __name__,
)

@profile_bp.before_request
def load_user():

    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    print(g)
    print(type(g))
    for i in g:
        print(i)
    print('user_inf: ', user_inf)
    user = database.col_users.find_one({'_id': user_inf['id']})
    g.user = user


@profile_bp.route('/profile_safe')
def profile_future_client():
    # return 'Хотите стать клиентом - свяжитесь с нами'
    print(g.user)
    print(type(g))
    return render_template('profile/profile_future_client.html')


@profile_bp.route('/profile_owner')
def profile_owner():
    # return 'Вы наш клиент'
    print(g.user)
    print(type(g))
    return render_template('profile/profile_owner.html')


@profile_bp.route('/profile_worker')
def profile_worker():
    # return 'Вы сотрудник мойки'
    print(g.user)
    print(type(g))
    return render_template('profile/profile_worker.html')
