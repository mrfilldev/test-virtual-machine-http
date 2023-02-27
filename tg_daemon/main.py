import datetime
import asyncio
from aiogram import Bot, types
import pytz
from config.config import Config

CHANNEL_ID = int(Config.CHANNEL_ID)
bot = Bot(token=Config.BOT_TOKEN)
col = Config.col

tz = pytz.timezone('Europe/Moscow')
# создание даты, которая будет использоваться в качестве фильтра
date_filter = datetime.datetime(2023, 2, 28, 12, 0, 0, tzinfo=tz)

pipeline = [
    {"$match": {"BoxNumber": '1'}}
]


async def try_to_understand_mongo_db():
    # поиск документов в коллекции, соответствующих фильтру по дате
    #docs = col.aggregate(pipeline)
    #print('docs: ', type(docs), docs)
    for doc in col.aggregate(pipeline):
        print(doc)


async def main():
    await try_to_understand_mongo_db()


if __name__ == '__main__':
    print("RUNNING")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    loop.close()
    print("FINISHED")

##################################################
# s = await bot.get_session()
# await s.close()
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
