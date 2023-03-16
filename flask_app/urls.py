# -*- coding: utf-8 -*-
from datetime import date

import requests
from dateutil import parser
import traceback

import boto3
from bson import json_util
from flask import Flask, render_template, url_for, request, session, redirect, Response, jsonify, make_response
from requests import post

import carwash_list
import carwash_order
import ping_carwash_box
from config.config import Config
from flask_bootstrap import Bootstrap

import json
from types import SimpleNamespace
import bcrypt

from flask_app import oauth_via_yandex
from flask_app.carwashes import create_carwash_obj
from flask_app.specific_methods import method_of_filters
from forms import CarwashForm
from urllib.parse import urlencode

from flask_app.decorators.auth_decorator import login_required

# from authlib.integrations.flask_client import OAuth


# Идентификатор приложения
client_id = 'ИДЕНТИФИКАТОР_ПРИЛОЖЕНИЯ'
# Пароль приложения
client_secret = 'ПАРОЛЬ_ПРИЛОЖЕНИЯ'
# Адрес сервера Яндекс.OAuth
baseurl = 'https://oauth.yandex.ru/'

app = Flask(__name__,
            static_url_path='',
            static_folder='/static',
            # template_folder='/templates'
            )
bootstrap = Bootstrap(app)
# oauth = OAuth(app)

users = Config.col_users
orders = Config.col_orders
db_carwashes = Config.col_carwashes

URL_DEV = Config.URL_DEV
API_KEY = Config.API_KEY  # ['123456', '7tllmnubn49ghu5qrep97']

##################################################################
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


########################################################################
# google = oauth.register(
#     name='google',
#     client_id=Config.YAN_CLIENT_ID,
#     client_secret=Config.YAN_CLIENT_SECRET,
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     access_token_params=None,
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     api_base_url='https://www.googleapis.com/oauth2/v1/',
#     userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
#     client_kwargs={'scope': 'openid email profile'},
# )


# @app.route('/')
# def reg_yan_auth():
#     if request.args.get('code', False):
#         # Если скрипт был вызван с указанием параметра "code" в URL,
#         # то выполняется запрос на получение токена
#         print(request.args)
#         print(request.data)
#         data = {
#             'grant_type': 'authorization_code',
#             'code': request.args.get('code'),
#             'client_id': client_id,
#             'client_secret': client_secret
#         }
#         data = urlencode(data)
#         # Токен необходимо сохранить для использования в запросах к API Директа
#         return jsonify(post(baseurl + "token", data).json())
#     else:
#         # Если скрипт был вызван без указания параметра "code",
#         # то пользователь перенаправляется на страницу запроса доступа
#         return redirect(baseurl + "authorize?response_type=code&client_id={}".format(client_id))


########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################


@app.route('/carwash/ping')
async def return_carwash_ping():
    apiKey = request.args.get('apikey')
    print('try_apiKey: ' + apiKey)

    if apiKey in API_KEY:
        status = ping_carwash_box.main(request)
        response = Response(status=status, mimetype="application/json")

    else:
        result = 'Error, Something is wrong...'
        status = 401

        response = Response(result, status=status, mimetype="application/json")
    print(response)
    return response


@app.route('/carwash/list')
async def return_carwash_list():
    try_apiKey = request.args.get('apikey')
    print('try_apiKey: ' + try_apiKey)
    if try_apiKey in API_KEY:
        result = carwash_list.main(request)
        status = 200
    else:
        result = 'Error, Something is wrong...'
        status = 401
    response = Response(result, status=status, mimetype="application/json")
    return response


@app.route('/carwash/order', methods=['POST'])
@app.route('/tanker/order', methods=['POST'])
async def make_carwash_order():
    try:
        carwash_order.main(request)
        return Response(status=200)
    except Exception as e:
        # write to log
        traceback.print_exc()
        print(f'caught {type(e)}: e', e)  # добавить логгер
        return Response(status=400)


########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('main'))

    return render_template('users/index.html')


@app.route('/main')
def main():
    # get ya-token
    resp = oauth_via_yandex.get_code(request)
    for key in dict(session):
        print(key, ":", session[key])
    session['ya-token'] = resp['access_token']
    print('ya-token has been inserted')
    #get values of user
    #values_of_user = oauth_via_yandex.get_user(resp['access_token'])

    #resp = make_response(render_template("profile/profile.html"))
    resp = render_template("profile/profile.html")
    #resp.set_cookie('username', username)
    return render_template("profile/profile.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    try:
        if request.method == 'POST':
            existing_user = users.find_one({'name': request.form['username']})

            if existing_user is None:
                hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
                users.insert_one({'name': request.form['username'], 'password': hashpass})
                session['username'] = request.form['username']
                return redirect(url_for('index'))

            return 'That username already exists!'

        return render_template('users/register.html')
    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return 'Invalid username/password combination'


@app.route('/oauth')
def oauth():
    url: str = f'https://oauth.yandex.ru/authorize?response_type=code&client_id={Config.YAN_CLIENT_ID}&redirect_uri=http://test-tanker-carwash.ru/main'
    return redirect(url)


@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        username = request.form['username']
        password = request.form['pass'].encode('utf-8')
        user = users.find_one({'name': username})

        if user is None:
            return redirect(url_for('index'))  # , #ecode='101')
            # Получаем данные из формы
        # print('user', user)
        # print('pass', user['password'])

        if user and bcrypt.checkpw(password, user['password']):
            session['username'] = username
            return redirect(url_for('admin'))
        # return redirect(url_for('index'), ecode='102')

    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return 'Invalid username/password combination'


@app.route('/logout')
def logout():
    try:
        for key in list(session.keys()):
            session.pop(key)
        return redirect('/')

    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return 'Invalid username/password combination'


@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    all_orders = orders.find()  # { 'DateCreate: {gt: ''}' ; orderStatus: })
    if request.method == 'POST':
        find_arguments = method_of_filters(request)
        # parse
        all_orders = orders.find(find_arguments)
    orders_list = []
    count_orders = 0
    for count_orders, i in enumerate(list(all_orders)[::-1], 1):
        # count_orders += 1
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print(order_obj)
        orders_list.append(order_obj)
    today = date.today()
    context = {
        'orders_list': orders_list,
        'count_orders': count_orders,
        'date': today
    }
    return render_template(
        'admin_zone/admin.html',
        context=context
    )


@app.route('/test', methods=['POST', 'GET'])
def test():
    return render_template(
        'test.html',
    )


@app.route('/order_detail/<string:order_id>', methods=['POST', 'GET'])
@login_required
def order_detail(order_id):
    order_obj = orders.find_one({'Id': order_id})  # dict
    data = json.loads(json_util.dumps(order_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    location_my = {
        'latitude': 55.650378,
        'longitude': 37.606487
    }
    location_crystal = {
        'latitude': 55.750843,
        'longitude': 37.536693
    }
    if order_obj.CarWashId == '1':
        location = location_my
    else:
        location = location_crystal

    context = {
        'order': order_obj,
        'location': location
    }
    return render_template(
        'admin_zone/order_detail.html',
        context=context
    )


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    print(user_inf)
    return render_template('profile/profile.html', context=user_inf)


@app.route('/carwashes', methods=['GET'])
@login_required
def carwashes():
    carwashes_list = []
    all_orders = db_carwashes.find()
    count_carwashes = 0

    for count_carwashes, i in enumerate(all_orders, 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        carwashes_list.append(carwash_obj)
        print(carwash_obj)
    context = {
        'carwashes_list': carwashes_list,
        'count_carwashes': count_carwashes,

    }

    return render_template(
        'carwash/carwash_list.html',
        context=context
    )


@app.route('/create_carwash', methods=['GET', 'POST'])
@login_required
def create_carwash():
    form = CarwashForm()
    if request.method == 'POST':
        create_carwash_obj(form)

    return render_template("carwash/create_carwash.html", form=form)
    #    username = dict(session)['username']


@app.route('/carwash_detail/<string:carwash_id>', methods=['POST', 'GET'])
@login_required
def carwash_detail(carwash_id):
    return f'carwash_detil {carwash_id}'
    # order_obj = orders.find_one({'Id': order_id})  # dict
    # data = json.loads(json_util.dumps(order_obj))
    # data = json.dumps(data, default=lambda x: x.__dict__)
    # order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    # location = {
    #     'latitude': 55.650378,
    #     'longitude': 37.606487
    # }
    # context = {
    #     'order': order_obj,
    #     'location': location
    # }
    # return render_template(
    #     'admin_zone/order_detail.html',
    #     context=context
    # )


################################################################
@app.template_filter()
def format_datetime(value):
    # variant = value.strftime('%Y-%m-%d')
    # print(variant)
    if isinstance(value, date):
        value = value.strftime('%d.%m.%Y')
    else:
        value = parser.parse(value)
        value = value.strftime("%d.%m.%Y %H:%M:%S")
    return value


################################################################
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.run(host='127.0.0.1', port=8080)

#
