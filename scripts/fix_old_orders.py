import json
from types import SimpleNamespace

from bson import json_util

from config.config import Config

orders = Config.col_orders.find({})

for i in orders:
    order_dict = json.loads(json_util.dumps(i))
    carwash_obj = Config.col_carwashes.find_one({'Id': int(order_dict['CarWashId'])})  # dict
    print(carwash_obj)
    data = json.loads(json_util.dumps(carwash_obj))
    value = carwash_obj['Name']

    set_command = {
        "$set": {
            "name_of_carwash": str(value),
        },
    }
    orders.update_one({'Id': order_dict['Id']}, set_command)

