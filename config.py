import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    URL_DEV = os.environ.get('URL_DEV')
    API_KEY = ['123456', '7tllmnubn49ghu5qrep97']

    SECRET_KEY = os.environ.get('SECRET_KEY')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
