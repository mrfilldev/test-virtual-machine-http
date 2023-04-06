from flask import Flask
from flask_bootstrap import Bootstrap

from flask_login import LoginManager

from ..api.api import api_bp
from ..main.main import main_bp
from ..profile.profile import profile_bp

app = Flask(__name__,
            template_folder='..templates')
app.CSRF_ENABLED = True
app.DEBUG = False

bootstrap = Bootstrap(app)
login = LoginManager()
app.register_blueprint(api_bp)
app.register_blueprint(main_bp)
app.register_blueprint(profile_bp)






