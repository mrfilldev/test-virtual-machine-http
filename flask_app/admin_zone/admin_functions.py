import json
import traceback
from types import SimpleNamespace

from bson import json_util
from flask import render_template

from flask_app import oauth_via_yandex, carwashes
from config.config import Config
from ..carwashes import CategoryAuto


users = Config.col_users
prices = Config.col_prices


def check_root(session):
    """
    1. получить по токену сессии имя uid
    2. найти пользователя с uid в монге
    3. проверить его уровень допуска
    ________________________________________________________________

    :return:

    вернуть объект || вернуть цифру уровня допуска
    """
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    user_id = user_inf['id']
    user = users.find_one({'id': user_id})

    if user['access_level'] == 'admin':
        return 'admin'
    else:
        return 'user'


def admin_main(request, session):
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    inf_list = []
    for k in user_inf:
        inf_list.append(f"{k} -> {user_inf[k]} \n")
    print(user_inf)

    status = 'admin'
    context = {
        'user': user_inf,
        'inf_list': inf_list,
        'status': status

    }
    return render_template('admin_zone/admin_main.html', context=context)


def delete_user(request, session, user_id):
    users.delete_one({'id': user_id})


def test_view(session):
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    all_users = users.find({})
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


def show_list_price():
    all_prices = prices.find({})
    prices_list = []
    count_prices = 0
    for count_prices, i in enumerate(list(all_prices)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print(price_obj)
        prices_list.append(price_obj)
    print(prices_list)
    context = {
        'prices_list': prices_list,
        'count_prices': count_prices,
    }
    return context


def create_price(request):
    for i in request.form:
        print(i, request.form[i])
    form = request.form
    id = prices.count_documents({}) + 1
    name = form['name']
    description = form['description']
    cost = float(request.form['price'])
    costType = form['costType']

    for i in list(CategoryAuto):
        new_price = carwashes.Prices(
            id=id,
            name=name,
            description=description,
            category=i.name,
            cost=cost,
            costType=costType
        )
        print(new_price)
        # запись в бд
        # new_price = eval(json.dumps(new_price, default=lambda x: x.__dict__))
        # print(new_price)
        # print(type(new_price))
        # prices.insert_one(new_price)


def edit_price(request, price_id):
    print('1')
    form = request.form
    price_id = {'Id': int(price_id)}
    print('2')
    print('old_carwash: ', price_id)
    set_fields = {'$set': {
        'name': form['name'],
        'description': form['description'],
        'cost': form['price'],
        'costType': form['costType']

    }}
    new_price = prices.update_one(price_id, set_fields)
    print('UPDATE FIELDS: ', set_fields)
    print('UPDATE DATA: ', new_price)
    return new_price


def delete_price(price_id):
    prices.delete_one({'Id': int(price_id)})
    print('deleted price: ', price_id)
