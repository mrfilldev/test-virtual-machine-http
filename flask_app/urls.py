# -*- coding: utf-8 -*-
import time
from datetime import datetime, date

from dateutil import parser
import traceback

import boto3
from bson import json_util
from flask import Flask, render_template, url_for, request, session, redirect, Response

import carwash_list
import carwash_order
import ping_carwash_box
from config.config import Config
from flask_bootstrap import Bootstrap

import json
from types import SimpleNamespace
import bcrypt

from flask_app import oauth_via_yandex
from flask_app.admin_zone.admin_functions import check_root, admin_main, delete_user
from flask_app.carwashes import create_carwash_obj, update_carwash_obj
from flask_app.specific_methods import method_of_filters
from flask_app.decorators.auth_decorator import login_required, admin_status_required, owner_status_required

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
db_companies = Config.col_companies

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
    if 'ya-token' in session:
        return redirect(url_for('main'))
    return render_template('users/index.html')


@app.route('/pereprava')
def pereprava():
    root = check_root(session)
    print(root)
    if root == 'admin':
        return redirect(url_for('admin'))
    return redirect(url_for('index'))


@app.route('/admin_main')
@login_required
@admin_status_required
def admin():
    return admin_main(request, session)


@app.route('/admin_delete_user/<string:user_id>')
@admin_status_required
@login_required
def admin_delete_user(user_id):
    delete_user(request, session, user_id)
    return redirect(url_for('admin'))


@app.route('/user_detail/<string:user_id>', methods=['POST', 'GET'])
@login_required
@admin_status_required
def user_detail(user_id):
    if request.method == 'POST':
        new_value = request.form['access_level']
        set_command = {"$set": {"access_level": new_value}}
        old_user = {'id': str(user_id)}
        new_user = users.update_one(old_user, set_command)
        print('new_user', new_user)

    user_obj = users.find_one({'id': str(user_id)})  # dict
    print(user_obj)

    data = json.loads(json_util.dumps(user_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    user_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print(user_obj)
    context = {
        'user': user_obj,
    }
    return render_template(
        'admin_zone/user_detail.html',
        context=context
    )


@app.route('/add_company/', methods=['POST', 'GET'])
@admin_status_required
def add_company():
    if request.method == 'POST':
        inn = request.form['inn']
        format = '%Y-%m-%dT%H:%M:%S%Z'
        db_companies.insert_one(
            {
                "_id": inn,
                "date": str(datetime.strptime(time.strftime(format, time.localtime()), format))
            }
        )
        print(f"Successfully added company {inn}")
        # return redirect(url_for('profile'))
    return render_template('admin_zone/add_company.html')


@app.route('/main')
def main():
    # get ya-token
    try:
        if 'ya-token' not in session:
            resp = oauth_via_yandex.get_code(request)
            for key in dict(session):
                print(key, ":", session[key])
            session['ya-token'] = resp['access_token']
            print('ya-token has been inserted')
        user_inf = oauth_via_yandex.get_user(session['ya-token'])
        user = users.find_one({'id': user_inf['id']})

        if user is None:
            format = '%Y-%m-%dT%H:%M:%S%Z'
            date_now = datetime.strptime(time.strftime(format, time.localtime()), format)
            print(date_now)
            users.insert_one(
                {
                    'id': user_inf['id'],
                    'psuid': user_inf['psuid'],
                    'login': user_inf['login'],
                    'access_level': 'Новый пользователь',
                    'date_registered': str(date_now),
                    'company_name': '',
                    'inn': '',
                }
            )
            print(f'user {user_inf["login"]} has been inserted')

        return redirect(url_for('profile'))
    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return "ошибОчка на стороне сервера :("


@app.route('/oauth')
def oauth():
    url: str = f'https://oauth.yandex.ru/authorize?response_type=code&client_id={Config.YAN_CLIENT_ID}&redirect_uri=http://test-tanker-carwash.ru/main'
    return redirect(url)


@app.route('/logout')
@login_required
def logout():
    try:
        for key in list(session.keys()):
            session.pop(key)
        return redirect('/')

    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return 'Invalid username/password combination'


@app.route('/orders_list', methods=['POST', 'GET'])
@owner_status_required
def orders_list():
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
        'order/orders_list.html',
        context=context
    )


@app.route('/test', methods=['POST', 'GET'])
@login_required
def test():
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    all_users = users.find({})
    # all_orders = orders.find({})
    # all_carwashes = db_carwashes.find({})
    # all_companies = db_companies.find({})

    users_list = []
    count_users = 0
    for count_users, i in enumerate(list(all_users)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        user_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print(user_obj)
        users_list.append(user_obj)
    print(users_list)
    inf_list = []
    for k in user_inf:
        inf_list.append(f"{k} -> {user_inf[k]} \n")
    print(user_inf)
    context = {
        'user': user_inf,
        'inf_list': inf_list,
        'users_list': users_list,
        'count_users': count_users,
    }
    return render_template(
        'admin_zone/test.html',
        context=context
    )


@app.route('/order_detail/<string:order_id>', methods=['POST', 'GET'])
@owner_status_required
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
        'order/order_detail.html',
        context=context
    )


@app.route('/profile/', methods=['POST', 'GET'])
@login_required
def profile():
    user_yan_inf = oauth_via_yandex.get_user(session['ya-token'])

    if request.method == 'POST':
        company_name = request.form['company_name']
        inn = request.form['inn']
        print('company_name: ', company_name)
        print('inn: ', inn)
        company = db_companies.find_one({'_id': inn})
        if company is not None:
            set_command = {
                "$set": {
                    "company_name": company_name,
                    "inn": inn,
                    "access_level": "Владелец сети"
                },
            }
            users.update_one({'id': user_yan_inf['id']}, set_command)
            db_companies.delete_one({'_id': inn})
        else:
            set_command = {
                "$set": {
                    "company_name": company_name,
                    "inn": inn,
                },
            }
            users.update_one({'id': user_yan_inf['id']}, set_command)
    status = ''
    user = users.find_one({'id': user_yan_inf['id']})
    data = json.loads(json_util.dumps(user))
    data = json.dumps(data, default=lambda x: x.__dict__)
    user = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    if user.access_level == 'Новый пользователь':
        status = 'new_user'
    elif user.access_level == 'Владелец сети':
        status = 'owner'

    elif user.access_level == 'admin':
        status = 'admin'

    context = {
        'status': status,
        'user': user,
        'user_yan_inf': user_yan_inf,
    }
    return render_template('profile/profile.html', context=context)


@app.route('/carwashes', methods=['POST', 'GET'])
@owner_status_required
def carwashes():
    carwashes_list = []
    all_carwashes = db_carwashes.find()
    count_carwashes = 0

    for count_carwashes, i in enumerate(list(all_carwashes)[::-1], 1):
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


@app.route('/create_carwash', methods=['POST', 'GET'])
@owner_status_required
def create_carwash():
    if request.method == 'POST':
        create_carwash_obj(request)
        return redirect(url_for('carwashes'))
    return render_template("carwash/create_carwash.html")


@app.route('/carwash_detail/<string:carwash_id>', methods=['POST', 'GET'])
@owner_status_required
def carwash_detail(carwash_id):
    if request.method == 'POST':
        new_carwash = update_carwash_obj(request, carwash_id)
        print('new carwash: ', new_carwash)
        return redirect(url_for('carwashes'))
    print(type(carwash_id))
    carwash_obj = db_carwashes.find_one({'Id': int(carwash_id)})  # dict
    print(carwash_obj)
    data = json.loads(json_util.dumps(carwash_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    amount_boxes = len(carwash_obj.Boxes)
    context = {
        'carwash': carwash_obj,
        'amount_boxes': amount_boxes
    }
    return render_template("carwash/carwash_detail.html", context=context)


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
