import asyncio
from aiogram import Bot, types
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus as quote
import pymongo

# from daemon.start_point import dbs

load_dotenv()

CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
bot = Bot(token=os.getenv('BOT_TOKEN'))

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

mycol = dbs.tst_items.mycol


async def get_today_collections():
    message = 'Всего коллекций в бд: '
    filter_date = {"DateCreate": {"$gt": "2023-02-24 ", "$lt": "2023-02-25"}}
    result = ''
    for order in mycol.find(filter=filter_date):
        result += str(order)
    result = message + result
    return result


async def get_amount_collections():
    message = 'Всего коллекций в бд: '
    amount_collections = dbs.list_collection_names()  # _documents()
    result = message + str(amount_collections)
    return result


async def get_one_order():
    message = 'Один заказ: '
    order = dbs.tst_items.mycol.find_one()
    result = message + str(order)
    return result


async def get_amount_orders():
    message = 'Всего заказов: \n'
    for post in dbs.tst_items.mycol.find():
        message += str(post) + '\n'  # _documents()

    if len(message) > 4000:
        for x in range(0, len(message), 4000):
            await bot.send_message(CHANNEL_ID, message[x:x + 4000])
    else:
        await bot.send_message(CHANNEL_ID, message)
    result = message
    return result


async def all_deffs():
    await bot.send_message(CHANNEL_ID, await get_amount_collections())
    await bot.send_message(CHANNEL_ID, await get_one_order())
    #await get_amount_orders()
    await get_today_collections()


async def main():
    await all_deffs()
    s = await bot.get_session()
    await s.close()


if __name__ == '__main__':
    print("RUNNING")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    loop.close()
    print("FINISHED")
