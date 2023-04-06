from flask_login import LoginManager

from . import app
from . import models
from . import configuration
from .db import database


login = LoginManager(app)
