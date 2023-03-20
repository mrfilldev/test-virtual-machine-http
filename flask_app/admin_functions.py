from flask_app import oauth_via_yandex
from config.config import Config


users = Config.col_users


def check_root(session):
    """
    1. получить по токену сессии имя uid
    2. найти пользователя с uid в монге
    3. проверить его уровень допуска
    ________________________________________________________________

    :return:

    вернуть объект || вернуть цифру уровня допуска
    """
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    user_id = user_inf['id']
    user = users.find_one({'id': user_id})


    pass