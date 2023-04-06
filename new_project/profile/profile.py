import os
import traceback
from flask import Blueprint, request, Response
from configuration.config import Config

profile_bp = Blueprint(
    'profile_blueprint', __name__,
)


@profile_bp.route('/profile_safe')
def profile_future_client():
    return 'Хотите стать клиентом - свяжитесь с нами'
