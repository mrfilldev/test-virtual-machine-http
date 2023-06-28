import json
from types import SimpleNamespace

from bson import json_util
from flask import render_template

from ..db import database
from ..db.models import Types, NetworkCarwashAmountStatus


def deserialize_mongo_doc(document):
    data = json.loads(json_util.dumps(document))
    data = json.dumps(data, default=lambda x: x.__dict__)
    res_doc = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    return res_doc


def generate_dict_of_networks(g_user_flask):
    network_obj_list = []
    carwash_obj_list = []
    all_carwashes = database.col_carwashes.find({})
    for i in all_carwashes:
        carwash_obj_list.append(deserialize_mongo_doc(i))

    if 'networks' not in g_user_flask.user_db:
        network_list = database.col_networks.find({})
        for i in network_list:
            network_obj_list.append(deserialize_mongo_doc(i))
    else:
        network_list = database.col_networks.find({'_id': g_user_flask.user_db['networks'][0]})
        for i in network_list:
            network_obj_list.append(deserialize_mongo_doc(i))
    dict_of_networks = {}

    for network_obj in network_obj_list:
        carwash_list = []
        for carwash_obj in carwash_obj_list:
            if str(carwash_obj.network_id) == str(network_obj._id):
                carwash_list.append(carwash_obj)
        carwash_list_sorted = sorted(carwash_list, key=lambda x: x.Enable, reverse=False)
        dict_of_networks[network_obj.network_name] = carwash_list_sorted

    return dict_of_networks


def analyze_networks_statistics(dict_of_networks):
    dict_analitic = {}
    for network_obj in dict_of_networks:
        amount = 0
        enabled = 0
        disabled = 0
        array_of_carwashes = dict_of_networks[network_obj]
        for carwash_obj in array_of_carwashes:
            amount += 1
            if carwash_obj.Enable:
                enabled += 1
            else:
                disabled += 1
        dict_analitic[network_obj] = NetworkCarwashAmountStatus(amount, enabled, disabled)

    return dict_analitic


def enabled_to_rus_boolean(enable):
    if enable:
        return "Активна"
    else:
        return "Не активна"


def make_info_text(dict_of_networks):
    dict_info = {}
    string_of_network = ''
    for network_obj in dict_of_networks:
        array_of_carwashes = dict_of_networks[network_obj]
        for carwash_obj in array_of_carwashes:
            string_of_network += f'{carwash_obj.Name} {carwash_obj.Address} ' \
                                 f'Местоположение: {carwash_obj.Location.lat}, {carwash_obj.Location.lon} - ' \
                                 f'{enabled_to_rus_boolean(carwash_obj.Enable)} \n'
        dict_info[network_obj] = string_of_network
    return dict_info


def carwashes_monitoring(g_user_flask):
    dict_of_networks = generate_dict_of_networks(g_user_flask)


    dict_analitic = analyze_networks_statistics(dict_of_networks)
    print('dict_of_network_statistics: %s' % dict_analitic)
    dict_info_to_copy = make_info_text(dict_of_networks)

    context = {
        'dict_of_networks': dict_of_networks,
        'dict_analitic': dict_analitic,
        'dict_info_to_copy': dict_info_to_copy,
    }
    return render_template(
        'monitoring/monitoring_all_carwashes.html',
        context=context
    )
