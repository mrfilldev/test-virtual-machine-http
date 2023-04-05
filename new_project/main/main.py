import os
import traceback
from flask import Blueprint, request, Response, session, redirect, url_for, render_template
from configuration.config import Config

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
