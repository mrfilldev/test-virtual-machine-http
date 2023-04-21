import json
from types import SimpleNamespace

from bson import json_util
from flask import render_template

from ..db import database
from ..db.models import Types


def get_carwashes(g_user_flask):
    if 'networks' not in g_user_flask.user_db:
        all_carwashes = database.col_carwashes.find({})
        network_obj = None
    else:
        network = g_user_flask.user_db['networks'][0]
        all_carwashes = database.col_carwashes.find({'network_id': network})
        print('network:', network)
        network = database.col_networks.find({'_id': network})
        data = json.loads(json_util.dumps(network))
        data = json.dumps(data, default=lambda x: x.__dict__)
        network_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))[0]  # SimpleNamespace
        print('network_obj:', network_obj)

    carwashes_list = []
    count_carwashes = 0

    for count_carwashes, i in enumerate(list(all_carwashes)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        carwashes_list.append(carwash_obj)
        print(carwash_obj)
    print(carwashes_list)
    return carwashes_list


def carwashes_monitoring(g_user_flask):

    context = {
        'carwashes_list': get_carwashes(g_user_flask),
        'enum_type_list': print(list(Types)),
    }
    return render_template(
        'monitoring/all_carwashes.html',
        context=context
    )
