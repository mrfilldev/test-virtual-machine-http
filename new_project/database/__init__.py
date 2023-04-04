import os
from flask import Flask
import database


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    app.register_blueprint()

    return app
