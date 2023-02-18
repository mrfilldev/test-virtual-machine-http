import asyncio
from urllib.parse import quote_plus as quote
import pymongo

from dotenv import load_dotenv
import daemon

load_dotenv()

url = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
    user=quote('user1'),
    pw=quote('mrfilldev040202'),
    hosts=','.join([
        'rc1a-f0wss58juko3mx2p.mdb.yandexcloud.net:27018'
    ]),
    rs='rs01',
    auth_src='db1')
dbs = pymongo.MongoClient(
    url,
    tlsCAFile='/home/mrfilldev/.mongodb/root.crt')['db1']


async def main():
    order = await daemon.get_order_messege_queue()


if __name__ == '__main__':
    print("RUNNING")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    loop.close()
    print("FINISHED")
