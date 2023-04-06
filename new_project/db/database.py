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
db_test = client['test_database']

col_orders = db_test["test_orders"]
col_owners = db_test["test_owners"]
col_carwashes_admins = db_test["test_carwashes_admins"]
col_carwashes = db_test["test_carwashes"]
col_prices = db_test["test_prices"]
col_companies = db_test["test_companies"]
col_networks = db_test["test_networks"]
col_users = db_test["test_users"]
