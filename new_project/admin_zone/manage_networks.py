import json
import uuid
from types import SimpleNamespace

from bson import json_util
from flask import render_template

from ..db import database
from ..db.models import Network, User


def network_detail(request):
    print('\n################################################################\n')
    if request.method == 'POST':
        form = request.form
        id = uuid.uuid4().hex
        name: str = form['name']
        new_network = Network(_id=id, network_name=name)
        new_network_json = json.dumps(new_network, default=lambda x: x.__dict__)
        new_network_dict = json.loads(new_network_json)
        new_network_dict['_id'] = new_network_dict.pop('Id')

        database.col_networks.update_one(new_network_dict)
        print("Network inserted successfully")
    context = {

    }
    return render_template('admin/network_detail.html', context=context)


def list_networks():
    all_networks = database.col_networks.find({})
    networks_list = []
    count_networks = 0
    for count_networks, i in enumerate(list(all_networks)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print(price_obj)
        networks_list.append(price_obj)
    print(networks_list)
    context = {
        'network_list': networks_list,
        'count_networks': count_networks,
    }
    return render_template('admin/list_networks.html', context=context)
