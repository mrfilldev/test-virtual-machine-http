import json
from types import SimpleNamespace

from bson import json_util

from ..db import database

db_carwashes = database.col_carwashes
db_prices = database.col_prices
db_sets_of_prices = database.col_sets_of_prices


def rename_attributes(obj, old_name, new_name):
    obj.__dict__[new_name] = obj.__dict__.pop(old_name)
    return obj


def rename_attributes_of_prices(price_obj):
    price_obj = rename_attributes(price_obj, 'name', 'Name')
    price_obj = rename_attributes(price_obj, 'description', 'Description')
    price_obj = rename_attributes(price_obj, 'categoryPrice', 'CategoryList')
    for categoryPrice in price_obj.CategoryList:
        categoryPrice = rename_attributes(categoryPrice, 'category', 'Category')
        categoryPrice = rename_attributes(categoryPrice, 'sum', 'Cost')
        print('categoryPrice: ', categoryPrice)
    price_obj = rename_attributes(price_obj, 'status', 'Status')
    price_obj = rename_attributes(price_obj, 'costType', 'CostType')
    delattr(price_obj, 'set_id')
    delattr(price_obj, 'priceType')
    try:
        delattr(price_obj, 'last_edit')
    except AttributeError:
        pass
    print(price_obj)

    return price_obj


def format_any_obj_id_to_Id(obj):
    '''
    Format:
    форматирование _id объекта бд
    для API yan-tanker
    '''
    print(obj)
    setattr(obj, 'Id', obj._id)
    delattr(obj, '_id')
    return obj


def format_price_field(carwash_obj, dict_of_prices_set):
    print('carwash_obj.Price: ', carwash_obj.Price)
    if carwash_obj.Price == '(не указано)':
        carwash_obj.Price = []
    else:
        for key, value in dict_of_prices_set.items():
            if carwash_obj.Price == key:
                carwash_obj.Price = value
                break
    return carwash_obj


def format_everything(carwash_obj, dict_of_prices_set):
    carwash_obj = format_any_obj_id_to_Id(carwash_obj)
    print('carwash_obj changed _id to Id: \n', carwash_obj)

    carwash_obj = format_price_field(carwash_obj, dict_of_prices_set)
    print('carwash_obj formatted .Price: \n', carwash_obj)

    return carwash_obj


def demo_remake_prices(price_obj):
    print("\nprice_obj: \n", price_obj)

    return price_obj


def make_dict_of_set_with_prices(all_sets):
    dict_of_set_with_prices = {}

    for prices_set in all_sets:
        data = json.loads(json_util.dumps(prices_set))
        data = json.dumps(data, default=lambda x: x.__dict__)
        prices_set_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        all_prices = db_prices.find({'set_id': prices_set_obj._id})
        arr_all_prices = []
        for price in all_prices:
            data = json.loads(json_util.dumps(price))
            data = json.dumps(data, default=lambda x: x.__dict__)
            price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
            price_obj = format_any_obj_id_to_Id(price_obj)
            price_obj = rename_attributes_of_prices(price_obj)
            price_obj = demo_remake_prices(price_obj)
            arr_all_prices.append(price_obj)

        dict_of_set_with_prices[prices_set_obj._id] = arr_all_prices
        print('dict_of_set_with_prices: ', dict_of_set_with_prices)

    return dict_of_set_with_prices


def carwash_list_main():
    all_carwashes = db_carwashes.find({})
    all_sets = db_sets_of_prices.find({})

    dict_of_prices_set = make_dict_of_set_with_prices(all_sets)

    print('\n PRICES \n')
    array_of_carwashes = []
    print('\n#########')
    for carwash in all_carwashes:
        data = json.loads(json_util.dumps(carwash))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('carwash_obj stock: \n', carwash_obj)

        carwash_obj = format_everything(carwash_obj, dict_of_prices_set)
        if carwash_obj.Id == '7810324c8fea4af8bc3c3d6776cfc494':
            for attr, val in carwash_obj.__dict__.items():
                print(f'{attr}:    {val}\n')
            array_of_carwashes.append(carwash_obj)
            print('\n\n\n\n\n')
        else:
            pass
    print('\n#########')
    print('array_of_carwashes: ', array_of_carwashes)
    return json.dumps(array_of_carwashes, default=lambda x: x.__dict__)
