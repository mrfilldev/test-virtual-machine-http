import json
from types import SimpleNamespace

from bson import json_util

from ..db import database

db_carwashes = database.col_carwashes
db_prices = database.col_prices
db_sets_of_prices = database.col_sets_of_prices


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
        for key, value in dict_of_prices_set:
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


def make_dict_of_set_with_prices(all_sets, all_prices):
    dict_of_set_with_prices = {}
    arr_all_sets = []
    for prices_set in all_sets:
        data = json.loads(json_util.dumps(prices_set))
        data = json.dumps(data, default=lambda x: x.__dict__)
        prices_set_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        arr_all_sets.append(prices_set_obj)
    arr_all_prices = []
    for price in all_prices:
        data = json.loads(json_util.dumps(price))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        arr_all_prices.append(price_obj)

    print('arr_all_sets: ', arr_all_sets)
    print('arr_all_prices: ', arr_all_prices)

    return dict_of_set_with_prices


def carwash_list_main():
    all_carwashes = db_carwashes.find({})
    all_prices = db_prices.find({})
    all_sets = db_sets_of_prices.find({})

    dict_of_prices_set = make_dict_of_set_with_prices(all_sets, all_prices)

    print('\n PRICES \n')
    array_of_carwashes = []
    print('\n#########')
    for carwash in all_carwashes:
        data = json.loads(json_util.dumps(carwash))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print('carwash_obj stock: \n', carwash_obj)

        carwash_obj = format_everything(carwash_obj, dict_of_prices_set)

        for attr, val in carwash_obj.__dict__.items():
            print(f'{attr}:    {val}\n')
        array_of_carwashes.append(carwash_obj)
        print('\n\n\n\n\n')
    print('\n#########')
    print('array_of_carwashes: ', array_of_carwashes)




# def carwash_list_main():
#     all_carwashes = db_carwashes.find({})
#     array_of_carwashes = []
#     for obj in all_carwashes:
#         print(obj)
#         if '_id' in obj:
#             obj['Id'] = obj.pop('_id')
#
#         print('BEFORE: ', obj['Price'])
#         # метод получения всех требуемых данных:
#         obj['Price'] = make_price_corrrect_4_tanker(obj['Price'])
#         print('AFTER: ', obj['Price'])
#         array_of_carwashes.append(obj)
#
#     # print('================================================================')
#     # print(array_of_carwashes)
#     # print('================================================================')
#     result = json.dumps(array_of_carwashes, default=lambda x: x.__dict__)
#
#     # print(result)
#     return result
#
#
# def make_price_corrrect_4_tanker(list_price):
#     result = []
#     for obj_price in list_price:
#         price_db_obj = db_prices.find({'_id': obj_price['_id']})
#         data = json.loads(json_util.dumps(price_db_obj))
#         data = json.dumps(data, default=lambda x: x.__dict__)
#         price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))[0]  # SimpleNamespace
#         print('price from web_params:\n', price_obj)
#         print('price already in carwash web_params:\n', obj_price)
#         # Поля которые требуется сформировать
#         # Id Name Description Category Cost CostType
#         result.append({
#             'Id': str(obj_price['_id'] + '_' + obj_price['categoryPrice']),
#             'Name': price_obj.name,
#             'Description': price_obj.description,
#             'Category': obj_price['categoryPrice'],
#             'Cost': obj_price['cost'],
#             'CostType': price_obj.costType,
#         })
#
#     return result
