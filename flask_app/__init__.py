from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from flask_app import urls, carwash_list, carwash_order, ping_carwash_box, forms, carwashes, models

from config import config

app = Flask(
    __name__,
    static_url_path='',
    static_folder='/static',
)
login_manager = LoginManager(app)
bootstrap = Bootstrap(app)