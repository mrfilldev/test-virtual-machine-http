from flask import Flask
from flask_bootstrap import Bootstrap

from db import database

from flask_login import LoginManager

from new_project.api.api import api_bp
from .main.main import main_bp
from .profile.profile import profile_bp

app = Flask(__name__)
app.CSRF_ENABLED = True
app.DEBUG = False

bootstrap = Bootstrap(app)
login = LoginManager()
app.register_blueprint(api_bp)
app.register_blueprint(main_bp)
app.register_blueprint(profile_bp)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    #app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.run(host='127.0.0.1', port=8080)




