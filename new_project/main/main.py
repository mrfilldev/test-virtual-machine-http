import os

import time
import traceback
from datetime import datetime, date


from flask import Blueprint, request, Response, session, redirect, url_for, render_template
from configuration.config import Config
from db import database


from . import oauth_via_yandex

main_bp = Blueprint(
    'main_blueprint', __name__,
)


@main_bp.route('/oauth')
def oauth():
    print(Config.YAN_CLIENT_ID)

    url: str = f'https://oauth.yandex.ru/authorize?response_type=code' \
               f'&client_id={Config.YAN_CLIENT_ID}' \
               f'&redirect_uri=http://test-tanker-carwash.ru/main'
    return redirect(url)


@main_bp.route('/')
def index():
    if 'ya-token' in session:
        return redirect(url_for('main'))
    else:
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
        print('user: ', user)
        if user is None:
            format = '%Y-%m-%dT%H:%M:%S%Z'
            date_now = datetime.strptime(time.strftime(format, time.localtime()), format)
            print(date_now)
            print({
                '_id': user_inf['id'],
                'psuid': user_inf['psuid'],
                'login': user_inf['login'],
                'access_level': 'Новый пользователь',
                'date_registered': str(date_now),
                'company_name': '',
                'inn': '',
            })

            # Config.col_users.insert_one(
            #     {
            #         '_id': user_inf['id'],
            #         'psuid': user_inf['psuid'],
            #         'login': user_inf['login'],
            #         'access_level': 'Новый пользователь',
            #         'date_registered': str(date_now),
            #         'company_name': '',
            #         'inn': '',
            #     }
            # )
            print(f'user {user_inf["login"]} has been inserted')

        return redirect(url_for('profile'))
    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return "ошибОчка на стороне сервера :("
