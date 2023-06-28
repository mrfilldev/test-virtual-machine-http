import os

import boto3
from dotenv import load_dotenv

load_dotenv()  # TESTING


class Config(object):
    URL_DEV = os.environ.get('URL_DEV')
    API_KEY = os.environ.get('API_KEY')

    SECRET_KEY = os.environ.get('SECRET_KEY')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    CHANNEL_ID = os.environ.get('CHANNEL_ID')
    BOT_TOKEN = os.environ.get('BOT_TOKEN')

    # yandex oauth
    YAN_CLIENT_ID = os.environ.get('TESTING_YAN_CLIENT_ID')
    YAN_CLIENT_SECRET = os.environ.get('TESTING_YAN_CLIENT_SECRET')


class Sqs_params:
    client = boto3.client(
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,  # os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,  # os.getenv('AWS_SECRET_ACCESS_KEY'),
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1'
    )
    queue_url = client.create_queue(QueueName='test-tanker-carwsh-orders').get('QueueUrl')
