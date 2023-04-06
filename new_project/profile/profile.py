import os
import traceback
from flask import Blueprint, request, Response, render_template
from ..configuration.config import Config

profile_bp = Blueprint(
    'profile_blueprint', __name__,
)


@profile_bp.route('/profile_safe')
def profile_future_client():
    # return 'Хотите стать клиентом - свяжитесь с нами'
    return render_template('profile/profile_future_client.html')


@profile_bp.route('/profile_owner')
def profile_owner():
    # return 'Вы наш клиент'
    return render_template('profile/profile_owner.html')


@profile_bp.route('/profile_owner')
def profile_worker():
    # return 'Вы сотрудник мойки'
    return render_template('profile/profile_worker.html')
