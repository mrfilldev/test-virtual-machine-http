from urllib.parse import quote_plus as quote
import pymongo

# pymongo
url = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
    user=quote('user1'),
    pw=quote('mrfilldev040202'),
    hosts=','.join([
        'rc1a-f0wss58juko3mx2p.mdb.yandexcloud.net:27018'
    ]),
    rs='rs01',
    auth_src='production_db')
client = pymongo.MongoClient(
    url,
    tlsCAFile='/home/mrfilldev/.mongodb/root.crt')
db_test = client['production_db']

col_orders = db_test["production_orders"]
col_owners = db_test["production_owners"]
col_carwashes_admins = db_test["production_carwashes_admins"]
col_carwashes = db_test["production_carwashes"]
col_prices = db_test["production_prices"]
col_sets_of_prices = db_test["production_sets_of_prices"]
col_companies = db_test["production_companies"]
col_networks = db_test["production_networks"]
col_users = db_test["production_users"]
