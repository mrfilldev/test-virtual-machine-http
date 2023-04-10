import time
import traceback
from datetime import datetime

from flask import Blueprint, request, session, redirect, url_for, render_template, g
from flask_login import login_required

# from ..app import login
from ..configuration.config import Config

from . import oauth_via_yandex
from ..db import database

from ..db.models import User

main_bp = Blueprint(
    'main_blueprint', __name__,
)


@main_bp.route('/oauth', methods=['POST', 'GET'])
def oauth():
    print(Config.YAN_CLIENT_ID)
    if request.method == 'POST':
        form = request.form
        url: str = f'https://oauth.yandex.ru/authorize?response_type=code' \
                   f'&client_id={Config.YAN_CLIENT_ID}' \
                   f'&redirect_uri=http://test-tanker-carwash.ru/main' \
                   f'&name={form["name"]}' \
                   f'&surname={form["surname"]}' \
                   f'&phone_number={form["phone_number"]}' \
                   f'&network_name={form["network_name"]}'

        print('url_to_redirrect:', url)
        return redirect(url)
    else:
        return redirect('/')


@main_bp.route('/')
def index():
    if 'ya-token' in session:
        return redirect(url_for('main_blueprint.main'))
    else:
        # if request.method == 'POST':
        #     phone = request.form['phone']
        #

        return render_template('main/index.html')


@main_bp.route('/main')
def main():
    # get ya-token
    try:
        if 'ya-token' not in session:
            resp = oauth_via_yandex.get_code(request)
            for key in dict(session):
                print(key, ":", session[key])
            session['ya-token'] = resp['access_token']
            print('ya-token has been inserted')
        print('ya-token is True')
        user_inf = oauth_via_yandex.get_user(session['ya-token'])
        print('user_inf: ', user_inf)
        user = database.col_users.find_one({'_id': user_inf['id']})
        print(user)
        # network = database.col_networks.find_one({'owner_id': user_inf['id']})
        # print(network)
        if user is None:
            # if network is not None:
            format = '%Y-%m-%dT%H:%M:%S%Z'
            date_now = datetime.strptime(time.strftime(format, time.localtime()), format)
            print(date_now)
            database.col_users.insert_one(
                {
                    '_id': user_inf['id'],
                    'email': user_inf['default_email'],
                    'login': user_inf['login'],
                    'number': user_inf['default_phone']['number'],
                    'date_registered': str(date_now),
                    'role': 'network_owner',
                }
            )
            print(f'user {user_inf["login"]} has been inserted')
        # else:
        #     format = '%Y-%m-%dT%H:%M:%S%Z'
        #     date_now = datetime.strptime(time.strftime(format, time.localtime()), format)
        #     print(date_now)
        #     database.col_users.insert_one(
        #         {
        #             '_id': user_inf['id'],
        #             'email': user_inf['default_email'],
        #             'login': user_inf['login'],
        #             'number': user_inf['default_phone']['number'],
        #             'date_registered': str(date_now),
        #         }
        #     )
        #     print(f'user {user_inf["login"]} has been inserted')
        else:
            return redirect(url_for('profile_blueprint.profile'))
    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return "ошибОчка на стороне сервера :("


@main_bp.route('/logout')
def logout():
    try:
        for key in list(session.keys()):
            session.pop(key)
        return redirect('/')

    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return 'Invalid username/password combination'
