from datetime import timedelta, date
from dateutil import parser
from flask import render_template, request, Blueprint, session, g, url_for, redirect, abort

from .edit_data_in_db import list_all_cols_in_db
from .fix_buttons import fix_network_id_in_orders, back_carwashes_refresh_prices, remake_prices_to_set, \
    prices_to_active, set_all_prices_attr_price_types, set_all_carwash_full_type, set_sets_of_prices_to_one_network, \
    fix_box_number_value, fix_orders_fields, fix_sets, fix_date_users, fix_date_orders
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
    try:
        user_inf = oauth_via_yandex.get_user(session['ya-token'])
        g.user_inf = user_inf
        print('g.user_inf: ', g.user_inf)
        user = database.col_users.find_one({'_id': user_inf['id']})
        g.user_db = user
        print('g.user_db: :', g.user_db)
    except Exception as e:
        print("Exception: %s" % str(e))
        return abort(500)


@admin_bp.errorhandler(500)
def page_not_found(e):
    return render_template("error_page/500.html"), 500


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


@admin_bp.route('/remake_fix_box_number_value')
def remake_fix_box_number_value():
    return fix_box_number_value()


@admin_bp.route('/remake_fix_orders_fields')
def remake_fix_orders_fields():
    return fix_orders_fields()


@admin_bp.route('/remake_fix_sets')
def remake_fix_sets():
    return fix_sets()


@admin_bp.route('/remake_fix_date')
def remake_fix_date():
    return fix_date_users()


@admin_bp.route('/remake_fix_date_orders')
def remake_fix_date_orders():
    return fix_date_orders()


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
    try:
        print('value: %s' % value, type(value))
        value = (parser.parse(value) + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M:%S")
        return value
    except Exception as e:
        print(e)
        return value


@admin_bp.app_template_filter()
def format_datetime_to_dmy(value):
    try:
        value = (parser.parse(value) + timedelta(hours=3)).strftime("%d.%m.%Y")
        return value
    except Exception as e:
        print(e)
        return value


@admin_bp.app_template_filter()
def format_datetime_to_HMS(value):
    try:
        value = (parser.parse(value) + timedelta(hours=3)).strftime("%H:%M:%S")
        return value
    except Exception as e:
        print(e)
        return value


@admin_bp.app_template_filter()
def format_datetime_to_HM(value):
    try:
        value = (parser.parse(value) + timedelta(hours=3)).strftime("%H:%M")
        return value
    except Exception as e:
        print(e)
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
        case 'LocalOrder':
            return 'Заказ контролируется администратором'
        case _:
            return value


@admin_bp.app_template_filter()
def format_category_car(value):
    match value:
        case 'Compact':
            return 'Кат.1'
        case 'MiddleSize':
            return 'Кат.2'
        case 'Crossover':
            return 'Кат.3'
        case 'OffRoad':
            return 'Кат.4'
        case 'MicroBus':
            return 'Кат.5'
        case _:
            return value


@admin_bp.app_template_filter()
def format_ContractId(value):
    match value:
        case 'OWN':
            return "Собственный заказ"
        case 'YARU':
            return "Внешний заказ"
        case _:
            return value


@admin_bp.app_template_filter()
def count_cost_bascket(bascket):
    try:
        total_cost = 0
        for obj in bascket:
            total_cost += obj.amount * obj.price
        return float(total_cost)
    except Exception as e:
        print(e)
        return bascket


@admin_bp.app_template_filter()
def format_space_numbers(value):
    try:
        ans = '{0:,}'.format(value).replace(',', ' ') + '0'
        print('ans: ', ans, type(ans))
        return ans
    except Exception as e:
        print(e)
        return value