import boto3
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from config.config import Config

app = Flask(
    __name__,
    static_url_path='',
    static_folder='/static',
)
bootstrap = Bootstrap(app)
login_manager = LoginManager()

def create_app():
    # Идентификатор приложения
    client_id = 'ИДЕНТИФИКАТОР_ПРИЛОЖЕНИЯ'
    # Пароль приложения
    client_secret = 'ПАРОЛЬ_ПРИЛОЖЕНИЯ'
    # Адрес сервера Яндекс.OAuth
    baseurl = 'https://oauth.yandex.ru/'
    # Конфиг приложения

    users = Config.col_owners
    orders = Config.col_orders
    db_carwashes = Config.col_carwashes
    prices = Config.col_prices
    db_companies = Config.col_companies

    URL_DEV = Config.URL_DEV
    API_KEY = Config.API_KEY

    # SQS MESSAGE QUEUE CONFIGURATION
    queue_orders = 'https://message-queue.api.cloud.yandex.net/b1gjm9f9sf1pbis8lhhp/dj600000000bqnoc01b1/test-tanker' \
                   '-carwsh-orders'

    client = boto3.client(
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,  # os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,  # os.getenv('AWS_SECRET_ACCESS_KEY'),
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1'
    )
    queue_url = client.create_queue(QueueName='test-tanker-carwsh-orders').get('QueueUrl')
    login_manager.init_app(app)
    with app.app_context():
        from . import routes

        # Register Blueprints
        app.register_blueprint(routes.app)

        return app