import json
from types import SimpleNamespace

from bson import json_util

from ..db import database

db_carwashes = database.col_carwashes
db_prices = database.col_prices


def carwash_list_main():
    all_carwashes = db_carwashes.find({})
    array_of_carwashes = []
    for carwash in all_carwashes:
        data = json.loads(json_util.dumps(carwash))
        data = json.dumps(data, default=lambda x: x.__dict__)
        carwash_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

        print('carwash_obj:\n')
        for attr, val in carwash_obj.__dict__.items():
            print(f'attr:    {attr}', f'val :    {val}')
        print('\n\n')
        array_of_carwashes.append(carwash_obj)

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
