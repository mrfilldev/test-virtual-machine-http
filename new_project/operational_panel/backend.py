import json
from types import SimpleNamespace

from bson import json_util
from flask import render_template

from new_project.db import database
from new_project.db.models import BoxStatusModel


def get_carwash_obj(carwash_id):
    carwash_obj = database.col_carwashes.find_one({'_id': carwash_id})  # dict
    data = json.loads(json_util.dumps(carwash_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    print('carwash_obj: ', carwash_obj)
    return carwash_obj




def view_boxes(request, carwash_id, g_flask_user):
    carwash_obj = get_carwash_obj(carwash_id)
    print(carwash_obj)
    context = {
        'carwash_obj': carwash_obj,
        'status_model': BoxStatusModel,
    }
    return render_template('operation_panel/view_boxes.html', context=context)



