from datetime import date

from dateutil import parser
from flask import render_template, request, Blueprint, session, g

from .edit_data_in_db import list_all_cols_in_db
from .manage_networks import list_networks, network_detail, add_network
from .manage_prices import show_list_price, create_price, edit_price, delete_price
from .manage_users import users_list_view, user_detail, delete_user
from ..db import database
from ..main import oauth_via_yandex

admin_bp = Blueprint(
    'admin_blueprint', __name__,
)


@admin_bp.before_request
def load_user():
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    print(g)
    print(type(g))
    for i in g:
        print(i)
    print('user_inf: ', user_inf)
    g.user_inf = user_inf
    print(g.user_inf)
    user = database.col_users.find_one({'_id': user_inf['id']})
    g.user_db = user
    print(g.user_db)


@admin_bp.route('/admin')
def admin_main():
    user_inf = oauth_via_yandex.get_user(session['ya-token'])
    inf_list = []
    for k in user_inf:
        inf_list.append(f"{k} -> {user_inf[k]} \n")
    print(user_inf)

    context = {
    }
    return render_template('admin/admin_profile.html', context=context)


@admin_bp.route('/users')
def admin_users():
    return users_list_view()


@admin_bp.route('/admin_user_detail/<string:user_id>', methods=['POST', 'GET'])
def admin_user_detail(user_id):
    return user_detail(request, user_id)


@admin_bp.route('/admin_delete_user/<string:user_id>', methods=['POST', 'GET'])
def admin_delete_user(user_id):
    return delete_user(user_id)


@admin_bp.route('/admin_networks_list/')
def admin_networks_list():
    return list_networks()


@admin_bp.route('/admin_network/', methods=['POST', 'GET'])
def admin_add_network():
    return add_network(request)


@admin_bp.route('/admin_network/<string:network_id>', methods=['POST', 'GET'])
def admin_network_detail(network_id):
    return network_detail(request, network_id)


@admin_bp.route('/list_of_prices/')
def list_of_prices():
    return show_list_price()


@admin_bp.route('/create_price', methods=['POST', 'GET'])
def admin_create_price():
    return create_price(request)


@admin_bp.route('/price_detail/<string:price_id>', methods=['POST', 'GET'])
def admin_price_detail(price_id):
    return edit_price(request, price_id)


@admin_bp.route('/delete_price/<string:price_id>', methods=['POST', 'GET'])
def admin_delete_price(price_id):
    return delete_price(price_id)


@admin_bp.route('/list_of_prices/')
def list_db():
    return list_all_cols_in_db()


@admin_bp.app_template_filter()
def format_datetime(value):
    # variant = value.strftime('%Y-%m-%d')
    # print(variant)
    if isinstance(value, date):
        value = value.strftime('%d.%m.%Y')
    else:
        value = parser.parse(value)
        value = value.strftime("%d.%m.%Y %H:%M:%S")
    return value

# def show_list_price():
#     all_prices = prices.find({})
#     prices_list = []
#     count_prices = 0
#     for count_prices, i in enumerate(list(all_prices)[::-1], 1):
#         data = json.loads(json_util.dumps(i))
#         data = json.dumps(data, default=lambda x: x.__dict__)
#         price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
#         print(price_obj)
#         prices_list.append(price_obj)
#     print(prices_list)
#     context = {
#         'prices_list': prices_list,
#         'count_prices': count_prices,
#     }
#     return context
#
#
# def create_price(request):
#     for i in request.form:
#         print(i, request.form[i])
#     form = request.form
#     id = prices.count_documents({}) + 1
#     name = form['name']
#     categoryPrice = []
#     description = form['description']
#     costType = form['costType']
#
#     for i in list(CategoryAuto):
#         categoryPrice.append(CostIdSum(i.name, form[str(i.name)]))
#
#     new_price = carwashes.Prices(id, name, description, categoryPrice, costType)
#
#     print(new_price.categoryPrice)
#     for i in new_price.categoryPrice:
#         print(f'{i.category} -> {i.sum}')
#
#     # запись в бд
#     new_price = eval(json.dumps(new_price, default=lambda x: x.__dict__))
#     print(new_price)
#     print(type(new_price))
#     prices.insert_one(new_price)
#
#
# def edit_price(request, price_id):
#     for i in request.form:
#         print(i, request.form[i])
#     print('1')
#     form = request.form
#     price_id = {'Id': int(price_id)}
#     print('2')
#     print('old_carwash: ', price_id)
#     categoryPrice = []
#     print(list(CategoryAuto))
#     for category in list(CategoryAuto):
#         print(category)
#         print(category.name)
#         print(form[str(category.name)])
#         categoryPrice.append(CostIdSum(category.name, form[str(category.name)]))
#     data = json.dumps(categoryPrice, default=lambda x: x.__dict__)
#     categoryPrice = json.loads(data)  # , object_hook=lambda d: SimpleNamespace(**d))
#     set_fields = {'$set': {
#         'name': form['name'],
#         'description': form['description'],
#         'categoryPrice': categoryPrice,
#         'costType': form['costType']
#
#     }}
#     new_price = prices.update_one(price_id, set_fields)
#     print('UPDATE FIELDS: ', set_fields)
#     print('UPDATE DATA: ', new_price)
#     return new_price
#
#
# def delete_price(price_id):
#     prices.delete_one({'Id': int(price_id)})
#     print('deleted price: ', price_id)
#
#
# def add_network(request):
#     print('\n################################################################\n')
#     form = request.form
#
#     id = uuid.uuid4().hex
#     name: str = form['name']
#
#     new_network = Network(_id=id, Name=name)
#
#     new_network_json = json.dumps(new_network, default=lambda x: x.__dict__)
#     new_network_dict = json.loads(new_network_json)
#     new_network_dict['_id'] = new_network_dict.pop('Id')
#
#     networks.insert_one(new_network_dict)
#     print("Network inserted successfully")
#
#
# def list_networks(request):
#     all_networks = networks.find({})
#     networks_list = []
#     count_networks = 0
#     for count_networks, i in enumerate(list(all_networks)[::-1], 1):
#         data = json.loads(json_util.dumps(i))
#         data = json.dumps(data, default=lambda x: x.__dict__)
#         price_obj = json.loads(data, object_hook=lambda d: Network(**d))
#         print(price_obj)
#         networks_list.append(price_obj)
#     print(networks_list)
#     context = {
#         'network_list': networks_list,
#         'count_networks': count_networks,
#     }
#     return context
#
#
# def add_user(request):
#     print('\n################################################################\n')
#     form = request.form
#
#     id = uuid.uuid4().hex
#
#     new_user = User(_id=id, Name='', Login=form['Login'], Network_Id=form['Network_Id'], Role=form['Role'])
#
#     new_user_json = json.dumps(new_user, default=lambda x: x.__dict__)
#     new_user_dict = json.loads(new_user_json)
#     new_user_dict['_id'] = new_user_dict.pop('Id')
#
#     users.insert_one(new_user_dict)
#     print("User inserted successfully")
