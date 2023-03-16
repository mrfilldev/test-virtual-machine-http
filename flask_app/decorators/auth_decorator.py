from flask import session, render_template, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('ya-token', None)
        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if user:
            # обмен на инф
            return f(*args, **kwargs)
        # выброс на авториз
        return redirect(url_for('oauth'))

    return decorated_function
