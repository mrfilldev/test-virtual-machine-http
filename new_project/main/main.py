import os
import traceback
from flask import Blueprint, request, Response, session, redirect, url_for, render_template
from configuration.config import Config

main_bp = Blueprint(
    'main_blueprint', __name__,
)


@main_bp.route('/')
def index():
    if 'ya-token' in session:
        return redirect(url_for('main'))
    else:
        return render_template('/templates/users/index.html')
