import json
from types import SimpleNamespace

from bson import json_util
from flask import redirect, url_for

from ..db import database


def list_orders(g):
    if 'networks' in g.user_db:
        network = g.user_db['networks'][0]
        all_carwashes = database.col_carwashes.find({'network_id': network})
        print('network:', network)
        network = database.col_networks.find({'_id': network})
        data = json.loads(json_util.dumps(network))
        data = json.dumps(data, default=lambda x: x.__dict__)
        network_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))[0]  # SimpleNamespace
        print('network_obj:', network_obj)

        orders_of_network = database.col_orders.find({'CarWashId': {'$in': network_obj.carwashes}})
    else:
        return redirect(url_for('/'))

    carwashes_list = []
    count_carwashes = 0