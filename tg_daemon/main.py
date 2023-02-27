import datetime
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
client = pymongo.MongoClient(
    url,
    tlsCAFile='/home/mrfilldev/.mongodb/root.crt')

db = client["study_use"]

col = db["mycollection"]


async def try_to_understand_mongo_db():
    # Вставка документа
    doc = {"name": "John", "age": 30}
    col.insert_one(doc)

    # Поиск документа
    doc = col.find_one({"name": "John"})
    print(doc)
    # Обновление документа
    col.update_one({"name": "John"}, {"$set": {"age": 31}})
    doc = col.find_one({"name": "John"})
    print(doc)
    # Удаление документа
    col.delete_one({"name": "John"})
    doc = col.find_one({"name": "John"})
    print(doc)


async def main():
    await try_to_understand_mongo_db()
    s = await bot.get_session()
    await s.close()


if __name__ == '__main__':
    print("RUNNING")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    loop.close()
    print("FINISHED")

##################################################
# #
#  message = 'Заказы за сутки: \n'
#     today_now = datetime.datetime.now()
#     delta = datetime.timedelta(days=1)
#     day_ago = (today_now - delta).isoformat()
#     filter_day = {"DateCreate": {"$gt": day_ago, "$lt": today_now}}
#
#
# async def get_amount_collections():
#     message = 'Всего коллекций в бд: '
#     amount_collections = dbs.list_collection_names()  # _documents()
#     result = message + str(amount_collections)
#     return result
#
#
# async def get_one_order():
#     message = 'Один заказ: '
#     order = dbs.tst_items.mycol.find().limit(1).sort({'$natural': '-1'})
#     result = message + str(order)
#     return result
#
#
# async def get_amount_orders():
#     message = 'Всего заказов: \n'
#     for post in dbs.tst_items.mycol.find():
#         message += str(post) + '\n'  # _documents()
#
#     if len(message) > 4000:
#         for x in range(0, len(message), 4000):
#             await bot.send_message(CHANNEL_ID, message[x:x + 4000])
#     else:
#         await bot.send_message(CHANNEL_ID, message)
#     result = message
#     return result
