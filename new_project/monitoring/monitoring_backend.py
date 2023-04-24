import json
from types import SimpleNamespace

from bson import json_util
from flask import render_template

from ..db import database
from ..db.models import Types


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
    print("carwash_obj_list: ", carwash_obj_list)
    if 'networks' not in g_user_flask.user_db:
        network_list = database.col_networks.find({})
        for i in network_list:
            network_obj_list.append(deserialize_mongo_doc(i))
    else:
        network_list = database.col_networks.find({'_id': g_user_flask.user_db['networks'][0]})
        for i in network_list:
            network_obj_list.append(deserialize_mongo_doc(i))
    print("network_obj_list: %s" % network_obj_list)
    dict_of_networks = {}

    for network_obj in network_obj_list:
        carwash_list = []
        for carwash_obj in carwash_obj_list:
            print("carwash_obj: %s" % carwash_obj)
            print("network_obj: %s" % network_obj)
            if str(carwash_obj.network_id) == str(network_obj._id):
                carwash_list.append(carwash_obj)
        print('network_obj: %s' % network_obj)
        dict_of_networks[network_obj.network_name] = carwash_list

    return dict_of_networks


def carwashes_monitoring(g_user_flask):
    dict_of_networks = generate_dict_of_networks(g_user_flask)
    print('dict_of_networks: %s' % dict_of_networks)
    context = {
        'dict_of_networks': dict_of_networks,
    }
    return render_template(
        'monitoring/monitoring_all_carwashes.html',
        context=context
    )
