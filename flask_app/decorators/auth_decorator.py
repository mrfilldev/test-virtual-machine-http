from flask import session, render_template, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('ya-token', None)
        if user:
            return f(*args, **kwargs)
        # выброс на авторизацию
        return redirect(url_for('oauth'))

    return decorated_function
