import json
from types import SimpleNamespace

from bson import json_util

from ..database import database

db_carwashes = database.col_carwashes
db_prices = database.col_prices


def carwash_list_main():
    all_carwashes = db_carwashes.find({})
    array_of_carwashes = []
    for obj in all_carwashes:
        if '_id' in obj:
            obj.pop('_id')

        print('BEFORE: ', obj['Price'])
        # метод получения всех требуемых данных:
        obj['Price'] = make_price_corrrect_4_tanker(obj['Price'])
        print('AFTER: ', obj['Price'])
        array_of_carwashes.append(obj)

    #     array_of_carwashes.append(obj)
    # print('================================================================')
    # print(array_of_carwashes)
    # print('================================================================')
    result = json.dumps(array_of_carwashes, default=lambda x: x.__dict__)
    # print(result)
    return result


def make_price_corrrect_4_tanker(list_price):
    result = []
    for obj_price in list_price:
        price_db_obj = db_prices.find({'Id': int(obj_price['Id'])})
        data = json.loads(json_util.dumps(price_db_obj))
        data = json.dumps(data, default=lambda x: x.__dict__)
        price_obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))[0]  # SimpleNamespace
        print('price from db:\n', price_obj)
        print('price already in carwash db:\n', obj_price)
        # Поля которые требуется сформировать
        # Id Name Description Category Cost CostType
        result.append({
            'Id': str(obj_price['Id'] + '_' + obj_price['categoryPrice']),
            'Name': price_obj.name,
            'Description': price_obj.description,
            'Category': obj_price['categoryPrice'],
            'Cost': obj_price['cost'],
            'CostType': price_obj.costType,
        })

    return result
