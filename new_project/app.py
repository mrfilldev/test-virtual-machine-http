#!/usr/bin/env python
import os
import sys
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from api.api import api_bp
from main.main import main_bp

app = Flask(
    __name__,
    static_url_path='',
    static_folder='/static',
    #template_folder='/templates'
)
app.CSRF_ENABLED = True
app.DEBUG = False
bootstrap = Bootstrap(app)
login_manager = LoginManager()
app.register_blueprint(api_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    #app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.run(host='127.0.0.1', port=8080)
