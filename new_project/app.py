#!/usr/bin/env python
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from api.api import api_bp

app = Flask(
    __name__,
    static_url_path='',
    static_folder='/static',

)
app.CSRF_ENABLED = True
bootstrap = Bootstrap(app)
login_manager = LoginManager()
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
