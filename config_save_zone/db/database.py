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
    auth_src='test_database')
client = pymongo.MongoClient(
    url,
    tlsCAFile='/home/mrfilldev/.mongodb/root.crt')
db_production = client['test_database']

col_orders = db_production["testing_orders"]
col_owners = db_production["testing_owners"]
col_carwashes_admins = db_production["testing_carwashes_admins"]
col_carwashes = db_production["testing_carwashes"]
col_prices = db_production["testing_prices"]
col_sets_of_prices = db_production["sets_of_prices"]
col_companies = db_production["testing_companies"]
col_networks = db_production["testing_networks"]
col_users = db_production["testing_users"]
