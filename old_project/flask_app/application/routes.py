"""Logged-in page routes."""
import json
from dateutil import parser

import time
import traceback
from datetime import datetime, date
from types import SimpleNamespace

from bson import json_util
from flask import Blueprint, redirect, render_template, url_for, request, Response, session
from flask_login import current_user, login_required
from old_project.config import Config
from flask_app import oauth_via_yandex
from old_project.flask_app import ping_carwash_box
from old_project.flask_app.admin_zone.admin_functions import check_root, admin_main, test_view, delete_user, show_list_price, \
    create_price, edit_price, prices, delete_price, add_network, list_networks, add_user
from flask_app.carwashes import carwash_list_main, CategoryAuto, create_carwash_obj, update_carwash_obj, db_carwashes, \
    delete_carwash_obj
from flask_app.decorators.auth_decorator import admin_status_required, owner_status_required
from old_project.flask_app.specific_methods import method_of_filters

# Blueprint Configuration
app = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)

@app.route('/carwash/ping')
async def return_carwash_ping():
    apiKey = request.args.get('apikey')
    print('try_apiKey: ' + apiKey)

    if apiKey in Config.API_KEY:
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
    if try_apiKey in Config.API_KEY:
        # result = carwash_list.main(request)
        result = carwash_list_main()
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
        # carwash_order.main(request)
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
    else:
        return render_template('users/../templates/users/index.html')


@app.route('/pereprava')
def pereprava():
    root = check_root(session)
    print(root)
    if root == 'admin':
        return redirect(url_for('admin'))
    return redirect(url_for('index'))


@app.route('/admin_main')
@admin_status_required
def admin():
    return admin_main(request, session)


@app.route('/test', methods=['POST', 'GET'])
@login_required
def test():
    return test_view(session)


@app.route('/admin_delete_user/<string:user_id>')
@admin_status_required
def admin_delete_user(user_id):
    delete_user(request, session, user_id)
    return redirect(url_for('admin'))


@app.route('/list_of_prices')
@admin_status_required
def list_of_prices():
    context = show_list_price()
    return render_template(
        '/admin_zone/prices/../templates/admin_zone/prices/prices_list.html',
        context=context
    )


@app.route('/create_price', methods=['POST', 'GET'])
@admin_status_required
def admin_create_price():
    if request.method == 'POST':
        create_price(request)
        return redirect(url_for('list_of_prices'))
    categories = []
    for i in list(CategoryAuto):
        categories.append(i.name)
    print('\nCATEGORY: ', categories, '\n')
    context = {
        'categories': categories,
    }
    return render_template('admin_zone/prices/../templates/admin_zone/prices/create_price.html', context=context)


@app.route('/edit_price/<string:price_id>', methods=['POST', 'GET'])
@admin_status_required
def admin_price_detail(price_id):
    if request.method == 'POST':
        new_price = edit_price(request, price_id)
        print('new price: ', new_price)
    price_obj = prices.find_one({'Id': int(price_id)})  # dict
    print('PRICE OOOOBJJJEEECTTT: ', price_obj)
    data = json.loads(json_util.dumps(price_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    context = {
        'price': price_obj,
    }
    return render_template('admin_zone/prices/../templates/admin_zone/prices/price_detail.html', context=context)


@app.route('/delete_price/<string:price_id>', methods=['POST'])
@admin_status_required
def admin_delete_price(price_id):
    delete_price(price_id)
    return redirect(url_for('list_of_prices'))


@app.route('/user_detail/<string:user_id>', methods=['POST', 'GET'])
@admin_status_required
def user_detail(user_id):
    if request.method == 'POST':
        new_value = request.form['access_level']
        set_command = {"$set": {"access_level": new_value}}
        old_user = {'_id': str(user_id)}
        new_user = Config.col_users.update_one(old_user, set_command)
        print('new_user', new_user)

    user_obj = Config.col_users.find_one({'_id': str(user_id)})  # dict
    print(user_obj)

    data = json.loads(json_util.dumps(user_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    user_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print(user_obj)
    context = {
        'users': user_obj,
    }
    return render_template(
        'admin_zone/../templates/admin_zone/user_detail.html',
        context=context
    )


@app.route('/add_company/', methods=['POST', 'GET'])
@admin_status_required
def add_company():
    if request.method == 'POST':
        inn = request.form['inn']
        format = '%Y-%m-%dT%H:%M:%S%Z'
        Config.col_companies.insert_one(
            {
                "_id": inn,
                "date": str(datetime.strptime(time.strftime(format, time.localtime()), format))
            }
        )
        print(f"Successfully added company {inn}")
        # return redirect(url_for('profile'))
    return render_template('admin_zone/../templates/admin_zone/add_company.html')


@app.route('/add_network/', methods=['POST', 'GET'])
@admin_status_required
def admin_add_network():
    if request.method == 'POST':
        add_network(request)
    return render_template('admin_zone/networks/../templates/admin_zone/networks/add_network.html')


@app.route('/list_networks/', methods=['POST', 'GET'])
@admin_status_required
def admin_networks():
    context = list_networks(request)
    return render_template('admin_zone/networks/../templates/admin_zone/networks/list_networks.html', context=context)


@app.route('/add_user/', methods=['POST', 'GET'])
@admin_status_required
def admin_add_user():
    if request.method == 'POST':
        add_user(request)

    return render_template('admin_zone/users/../templates/admin_zone/users/create_user.html')


########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################

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
        print('ya-token is True')
        user_inf = oauth_via_yandex.get_user(session['ya-token'])
        print('user_inf: ', user_inf)
        user = Config.col_users.find_one({'_id': user_inf['id']})
        print('users: ', user)
        if user is None:
            format = '%Y-%m-%dT%H:%M:%S%Z'
            date_now = datetime.strptime(time.strftime(format, time.localtime()), format)
            print(date_now)
            Config.col_users.insert_one(
                {
                    '_id': user_inf['id'],
                    'psuid': user_inf['psuid'],
                    'login': user_inf['login'],
                    'access_level': 'Новый пользователь',
                    'date_registered': str(date_now),
                    'company_name': '',
                    'inn': '',
                }
            )
            print(f'users {user_inf["login"]} has been inserted')

        return redirect(url_for('profile'))
    except Exception as e:
        traceback.print_exc()
        print(f'EXEPTION: \n{type(Exception)}: e', e)  # добавить логгер
        return "ошибОчка на стороне сервера :("


@app.route('/oauth')
def oauth():
    url: str = f'https://oauth.yandex.ru/authorize?response_type=code' \
               f'&client_id={Config.YAN_CLIENT_ID}' \
               f'&redirect_uri=http://test-tanker-carwash.ru/main'
    return redirect(url)


def login():
    return redirect(url_for('index'))


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
    all_orders = Config.col_users.find()  # { 'DateCreate: {gt: ''}' ; orderStatus: })
    if request.method == 'POST':
        find_arguments = method_of_filters(request)
        # parse
        all_orders = Config.col_orders.find(find_arguments)
    orders_list = []
    count_orders = 0
    distinctCarwashId = []
    for count_orders, i in enumerate(list(all_orders)[::-1], 1):
        # count_orders += 1
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        print(data)
        # order_obj = json.loads(data, object_hook=lambda d: Order(**d))
        order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print(vars(order_obj))
        orders_list.append(order_obj)
        if order_obj.CarWashId not in distinctCarwashId:
            distinctCarwashId.append(int(order_obj.CarWashId))

    # mongo find by filter in () // projections
    carwashes_names = []
    carwashes = Config.col_carwashes.find({"Id": {"$in": distinctCarwashId}}, {"Id": 1, "Name": 1})
    for i in carwashes:
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        carwashes_names.append(carwash)
    print(carwashes_names)
    for i in carwashes_names:
        print('carwashes_names: ', i)

    today = date.today()
    context = {
        'orders_list': orders_list,
        'count_orders': count_orders,
        'carwashes': carwashes_names,
        'date': today
    }
    return render_template(
        'order/../templates/order/orders_list.html',
        context=context
    )


@app.route('/order_detail/<string:order_id>', methods=['POST', 'GET'])
@owner_status_required
def order_detail(order_id):
    order_obj = Config.col_orders.find_one({'_id': order_id})  # dict
    data = json.loads(json_util.dumps(order_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    # order_obj = json.loads(data, object_hook=lambda d: Order(**d))  # SimpleNamespace
    print('order_obj: \n', order_obj)
    location_my = {
        'latitude': 55.650378,
        'longitude': 37.606487
    }
    location_crystal = {
        'latitude': 55.750843,
        'longitude': 37.536693
    }
    if order_obj.CarWashId == 1:
        location = location_my
    else:
        location = location_crystal
    context = {
        'order': order_obj,
        'location': location
    }
    return render_template(
        'order/../templates/order/order_detail.html',
        context=context
    )


@app.route('/profile/', methods=['POST', 'GET'])
@login_required
def profile():
    user_yan_inf = oauth_via_yandex.get_user(session['ya-token'])
    print('current_user: ', current_user)

    if request.method == 'POST':
        company_name = request.form['company_name']
        inn = request.form['inn']
        print('company_name: ', company_name)
        print('inn: ', inn)
        company = Config.col_companies.find_one({'_id': inn})
        if company is not None:
            set_command = {
                "$set": {
                    "company_name": company_name,
                    "inn": inn,
                    "access_level": "Владелец сети"
                },
            }
            Config.col_users.update_one({'id': user_yan_inf['id']}, set_command)
            Config.col_companies.delete_one({'_id': inn})
        else:
            set_command = {
                "$set": {
                    "company_name": company_name,
                    "inn": inn,
                },
            }
            Config.col_users.update_one({'id': user_yan_inf['id']}, set_command)
    status = ''
    user = Config.col_users.find_one({'_id': user_yan_inf['id']})
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
        'users': user,
        'user_yan_inf': user_yan_inf,
    }
    return render_template('profile/../templates/profile/profile.html', context=context)


@app.route('/carwashes', methods=['POST', 'GET'])
@owner_status_required
def carwashes():
    carwashes_list = []
    all_carwashes = Config.col_carwashes.find()
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
        'carwash/../templates/carwash/carwash_list.html',
        context=context
    )


@app.route('/create_carwash', methods=['POST', 'GET'])
@owner_status_required
def create_carwash():
    if request.method == 'POST':
        create_carwash_obj(request)
        return redirect(url_for('carwashes'))

    context = show_list_price()
    return render_template("carwash/../templates/carwash/create_carwash.html", context=context)


@app.route('/carwash_detail/<string:carwash_id>', methods=['POST', 'GET'])
@owner_status_required
def carwash_detail(carwash_id):
    if request.method == 'POST':
        new_carwash = update_carwash_obj(request, carwash_id)
        print('new carwash: ', new_carwash)
        return redirect(url_for('carwashes'))
    print(type(carwash_id))
    carwash_obj = db_carwashes.find_one({'_id': int(carwash_id)})  # dict
    print(carwash_obj)
    data = json.loads(json_util.dumps(carwash_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    amount_boxes = len(carwash_obj.Boxes)

    all_prices = prices.find()
    prices_list = []
    count_prices = 0
    for count_prices, i in enumerate(list(all_prices)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        prices_list.append(price_obj)
        print(price_obj)

    enum_list = list(CategoryAuto)
    print(enum_list)
    print('carwash_obj ', carwash_obj)
    context = {
        'carwash': carwash_obj,

        'amount_boxes': amount_boxes,
        'prices_list': prices_list,
        'count_prices': count_prices,
        'enum_list': enum_list
    }
    return render_template("carwash/../templates/carwash/carwash_detail.html", context=context)


@app.route('/delete_carwash/<string:carwash_id>', methods=['POST', 'GET'])
@owner_status_required
def delete_carwash(carwash_id):
    delete_carwash_obj(carwash_id)
    return redirect(url_for('carwashes'))


################################################################
@app.app_template_filter()
def format_datetime(value):
    # variant = value.strftime('%Y-%m-%d')
    # print(variant)
    if isinstance(value, date):
        value = value.strftime('%d.%m.%Y')
    else:
        value = parser.parse(value)
        value = value.strftime("%d.%m.%Y %H:%M:%S")
    return value


@app.app_template_filter()
def format_name_point(value):
    carwash_obj = db_carwashes.find_one({'Id': int(value)})  # dict
    print(carwash_obj)
    data = json.loads(json_util.dumps(carwash_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    value = carwash_obj.Name
    return value
