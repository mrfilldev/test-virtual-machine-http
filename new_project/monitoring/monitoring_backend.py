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
    if 'networks' not in g_user_flask.user_db:
        all_carwashes = database.col_carwashes.find({})
        network_list = database.col_networks.find({})
    else:
        all_carwashes = database.col_carwashes.find({})
        network_list = database.col_networks.find({'_id': g_user_flask.user_db['networks'][0]})

    dict_of_networks = {}

    for network in network_list:
        network_obj = deserialize_mongo_doc(network)
        carwash_list = []
        for carwash in all_carwashes:
            carwash_obj = deserialize_mongo_doc(carwash)
            if carwash_obj.network_id == network:
                carwash_list.append(carwash_obj)
        dict_of_networks[network_obj] = carwash_list

    return dict_of_networks


def carwashes_monitoring(g_user_flask):
    dict_of_networks = generate_dict_of_networks(g_user_flask)

    context = {
        'dict_of_networks': dict_of_networks,
    }
    return render_template(
        'monitoring/monitoring_all_carwashes.html',
        context=context
    )
