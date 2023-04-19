import json
from types import SimpleNamespace

from bson import json_util
from flask import url_for, redirect

from ..db import database


def fix_network_id_in_orders():
    all_orders = database.col_orders.find({})

    for order in all_orders:
        data = json.loads(json_util.dumps(order))
        data = json.dumps(data, default=lambda x: x.__dict__)
        order_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('order_obj: ', order_obj)
        current_carwash = database.col_carwashes.find_one({'_id': order_obj.CarWashId})
        data = json.loads(json_util.dumps(current_carwash))
        data = json.dumps(data, default=lambda x: x.__dict__)
        current_carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        if current_carwash_obj == None:
            database.col_orders.delete_one({'_id': order_obj._id})
            print('deleted order_id:', order_obj._id)
        else:
            print('current_carwash_obj: ', current_carwash_obj)
            old_order = {'_id': order_obj._id}
            set_fields = {'$set': {
                'network_id': current_carwash_obj.network_id,
            }}
            new_order = database.col_orders.update_one(old_order, set_fields)

    return redirect(url_for('admin_blueprint.admin_main'))
