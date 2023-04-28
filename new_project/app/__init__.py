from flask import Flask
from flask_bootstrap import Bootstrap

# from flask_login import LoginManager

from ..admin_zone.admin_profile import admin_bp
from ..configuration.config import Config
from ..api.api import api_bp
from ..main.main import main_bp
from ..profile.profile import profile_bp
from ..view_carwash.carwash import carwash_bp
from ..view_orders.order import order_bp
from ..monitoring.monitoring import monitoring_bp
from ..schedule.schedule import schedule_bp

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )
app.CSRF_ENABLED = True
app.DEBUG = False

bootstrap = Bootstrap(app)
# login = LoginManager()
# login.init_app(app)
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(main_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(carwash_bp)
app.register_blueprint(order_bp)
app.register_blueprint(monitoring_bp)
app.register_blueprint(schedule_bp)

app.config['SECRET_KEY'] = Config.SECRET_KEY

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='127.0.0.1', port=8080)
