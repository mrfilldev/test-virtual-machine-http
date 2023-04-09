import os
import traceback
from flask import Blueprint, request, Response, render_template, g, session, redirect, url_for
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
    g.user_inf = user_inf
    print('g.user_inf: ', g.user_inf)
    user = database.col_users.find_one({'_id': user_inf['id']})
    g.user_db = user
    print('g.user_db: :', g.user_db)


@profile_bp.route('/profile')
def profile():
    # return 'Хотите стать клиентом - свяжитесь с нами'
    print(g.user_db)
    print(g.user_inf)

    if 'role' not in g.user_db:
        return profile_future_client()
    else:
        if g.user_db['role'] == 'admin':
            return redirect(url_for('profile_blueprint.profile_admin'))
        elif g.user_db['role'] == 'network_owner':
            return redirect(url_for('profile_blueprint.profile_owner'))
        elif g.user_db['role'] == 'network_worker':
            return redirect(url_for('profile_blueprint.profile_worker'))


@profile_bp.route('/profile_safe')
def profile_future_client():
    # return 'Хотите стать клиентом - свяжитесь с нами'

    return render_template('profile/profile_future_client.html')


@profile_bp.route('/profile_owner')
def profile_owner():
    # return 'Вы наш клиент'

    return render_template('profile/profile_owner.html')


@profile_bp.route('/profile_worker')
def profile_worker():
    # return 'Вы сотрудник мойки'

    return render_template('profile/profile_worker.html')


@profile_bp.route('/admin')
def profile_admin():
    # return 'Вы admin'
    return redirect(url_for('admin_blueprint.admin_main'))
