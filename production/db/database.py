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
db_production = client['production_db']

col_orders = db_production["production_orders"]
col_owners = db_production["production_owners"]
col_carwashes_admins = db_production["production_carwashes_admins"]
col_carwashes = db_production["production_carwashes"]
col_prices = db_production["production_prices"]
col_sets_of_prices = db_production["production_sets_of_prices"]
col_companies = db_production["production_companies"]
col_networks = db_production["production_networks"]
col_users = db_production["production_users"]
