import json
import uuid
from types import SimpleNamespace

from bson import json_util
from flask import redirect, render_template, url_for

from ..db import database
from ..db.models import CategoryAuto, CostIdSum, Prices


def show_list_price():
    all_prices = database.col_prices.find({})
    prices_list = []
    count_prices = 0
    for count_prices, i in enumerate(list(all_prices)[::-1], 1):
        data = json.loads(json_util.dumps(i))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print(price_obj)
        prices_list.append(price_obj)
    print(prices_list)
    context = {
        'prices_list': prices_list,
        'count_prices': count_prices,
    }
    return render_template('admin/prices_list.html', context=context)


def create_price(request):
    if request.method == 'POST':
        for i in request.form:
            print(i, request.form[i])
        form = request.form
        id = uuid.uuid4().hex
        name = form['name']
        categoryPrice = []
        description = form['description']
        costType = form['costType']

        for i in list(CategoryAuto):
            categoryPrice.append(CostIdSum(i.name, form[str(i.name)]))

        new_price = Prices(id, name, description, categoryPrice, costType)

        print(new_price.categoryPrice)
        for i in new_price.categoryPrice:
            print(f'{i.category} -> {i.sum}')

        # запись в бд
        new_price = eval(json.dumps(new_price, default=lambda x: x.__dict__))
        print(new_price)
        print(type(new_price))
        new_price['_id'] = new_price.pop('Id')
        database.col_prices.insert_one(new_price)
        return redirect(url_for('admin_blueprint.list_of_prices'))

    categories = []
    for i in list(CategoryAuto):
        categories.append(i.name)
    print('\nCATEGORY: ', categories, '\n')
    context = {
        'categories': categories,
    }
    return render_template('admin/create_price.html', context=context)


def edit_price(request, price_id):
    if request.method == 'POST':
        for i in request.form:
            print(i, request.form[i])
        print('1')
        form = request.form
        price_id = {'_id': price_id}
        print('2')
        print('old_carwash: ', price_id)
        categoryPrice = []
        print(list(CategoryAuto))
        for category in list(CategoryAuto):
            print(category)
            print(category.name)
            print(form[str(category.name)])
            categoryPrice.append(CostIdSum(category.name, form[str(category.name)]))
        data = json.dumps(categoryPrice, default=lambda x: x.__dict__)
        categoryPrice = json.loads(data)  # , object_hook=lambda d: SimpleNamespace(**d))
        set_fields = {'$set': {
            'name': form['name'],
            'description': form['description'],
            'categoryPrice': categoryPrice,
            'costType': form['costType']

        }}
        new_price = database.col_prices.update_one(price_id, set_fields)
        print('UPDATE FIELDS: ', set_fields)
        print('UPDATE DATA: ', new_price)
        return redirect(url_for('admin_blueprint.list_of_prices'))

    price_obj = database.col_prices.find_one({'_id': price_id})  # dict
    print('PRICE OOOOBJJJEEECTTT: ', price_obj)
    data = json.loads(json_util.dumps(price_obj))
    data = json.dumps(data, default=lambda x: x.__dict__)
    price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))  # SimpleNamespace
    context = {
        'price': price_obj,
    }
    return render_template('admin/price_detail.html', context=context)


def delete_price(price_id):
    database.col_prices.delete_one({'_id': price_id})
    print('deleted price: ', price_id)
    return redirect(url_for('admin_blueprint.list_of_prices'))
