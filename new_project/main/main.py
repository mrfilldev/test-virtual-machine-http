import traceback

from flask import Blueprint, request, session, redirect, url_for, render_template, g
from flask_login import login_required

# from ..app import login
from ..configuration.config import Config

from . import oauth_via_yandex
from ..db import database

# from ..db.models import User

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
        return redirect(url_for('main_blueprint.main'))
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

        #print('user: ', g.user)
        # if user is None:
        # format = '%Y-%m-%dT%H:%M:%S%Z'
        # date_now = datetime.strptime(time.strftime(format, time.localtime()), format)
        # print(date_now)
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
        # print(f'user {user_inf["login"]} has been inserted')

        return redirect(url_for('profile_blueprint.profile_future_client'))
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
