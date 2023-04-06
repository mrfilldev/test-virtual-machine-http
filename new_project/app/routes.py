from app import app

from .api.api import api_bp
from .main.main import main_bp
from .profile.profile import profile_bp

app.register_blueprint(api_bp)
app.register_blueprint(main_bp)
app.register_blueprint(profile_bp)
