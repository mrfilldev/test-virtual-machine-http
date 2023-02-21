import asyncio
from aiogram import Bot, types
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus as quote
import pymongo
#from daemon.start_point import dbs

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


async def get_amount_orders():
    message = 'Всего заказов:'
    amount_orders = dbs.collection.find().count()
    result = message + amount_orders
    return result


async def main():
    await bot.send_message(
        CHANNEL_ID,
        await get_amount_orders()
    )
    s = await bot.get_session()
    await s.close()


if __name__ == '__main__':
    print("RUNNING")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    loop.close()
    print("FINISHED")
