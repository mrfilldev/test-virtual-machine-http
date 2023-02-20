from urllib.parse import quote_plus as quote

import ssl
import pymongo

url = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
    user=quote('user1'),
    pw=quote('mrfilldev040202'),
    hosts=','.join([
        'rc1a-f0wss58juko3mx2p.mdb.yandexcloud.net:27018'
    ]),
    rs='rs01',
    auth_src='test_16_02')
dbs = pymongo.MongoClient(
    url,
    tlsCAFile='/home/mrfilldev/.mongodb/root.crt')['test_16_02']

# c = dbs.orders.count();

# print(c)

x = dbs.tst_items.mycol.insert_one({"_id": 43, "value": 23, "sum": 9000.7, "name": 'vasya'});

print(x.inserted_id)

print(dbs.list_collection_names())

# print(dbs.tst_items.count())
# dbs.server_info()
# dbs.admin.command('{ ping: 1 }')
# dbs.test_collection.find(...)


################################################################
