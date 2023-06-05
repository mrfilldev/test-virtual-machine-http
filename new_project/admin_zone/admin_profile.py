from datetime import date

from dateutil import parser
from flask import render_template, request, Blueprint, session, g, url_for, redirect

from .edit_data_in_db import list_all_cols_in_db
from .fix_buttons import fix_network_id_in_orders, back_carwashes_refresh_prices, remake_prices_to_set, \
    prices_to_active, set_all_prices_attr_price_types, set_all_carwash_full_type, set_sets_of_prices_to_one_network
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


# @admin_bp.route('/delete_price/<string:price_id>', methods=['POST', 'GET'])
# def admin_delete_price(price_id):
#     return delete_price(price_id)


@admin_bp.route('/clear_sets/', methods=['POST', 'GET'])
def admin_clear_sets():
    return remake_prices_to_set()


@admin_bp.route('/carwashes_refresh_prices')
def carwashes_refresh_prices():
    return back_carwashes_refresh_prices()


@admin_bp.route('/remake_prices_to_active')
def remake_prices_to_active():
    return prices_to_active()


@admin_bp.route('/remake_prices_price_types')
def remake_prices_price_types():
    return set_all_prices_attr_price_types()


@admin_bp.route('/remake_all_carwash_full_type')
def remake_all_carwash_full_type():
    return set_all_carwash_full_type()


@admin_bp.route('/remake_set_sets_of_prices_to_one_network')
def remake_set_sets_of_prices_to_one_network():
    return set_sets_of_prices_to_one_network()


################################
################################
################################
################################
################################
################################
@admin_bp.route('/list_db')
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


@admin_bp.app_template_filter()
def format_status_order(value):
    match value:
        case 'OrderCreated':
            return 'Заказ создан'
        case 'Accepted':
            return 'Заказ в процессе'
        case 'Completed':
            return 'Заказ выполнен'
        case 'StationCanceled':
            return 'Заказ отменен мойкой'
        case 'UserCanceled':
            return 'Заказ отменен пользователем'
        case 'Expire':
            return 'Заказ не актуален'
        case 'SystemAggregator_Error':
            return 'Заказ не выполнен'
        case _:
            return value
