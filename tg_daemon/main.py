import datetime
import asyncio
from aiogram import Bot, types
import pytz
from config.config import Config
from datetime import datetime, timedelta, date

CHANNEL_ID = int(Config.CHANNEL_ID)
bot = Bot(token=Config.BOT_TOKEN)
col = Config.col_orders


# tz = pytz.timezone('Europe/Moscow')
# создание даты, которая будет использоваться в качестве фильтра
# date_filter = datetime.datetime(2023, 2, 28, 12, 0, 0, tzinfo=tz)


async def for_all_time():
    print("################################")
    start_time = str(datetime.now())

    print('start_time', type(start_time), start_time)
    pipeline = [
        # {"$match": {"DateCreateMy": {"$gte": start_time}}},
        {"$group": {"_id": "$Status",
                    # "CarWashId": "$CarWashId",
                    "total": {"$sum": "$Sum"},
                    "count": {"$sum": 1}}}
    ]
    result = col.aggregate(pipeline)

    # Выводим результаты
    message = "Сводка статусов заказов за все время:\n"
    for doc in result:
        print(doc)
        # message += f"{doc['CarWashId']}:\n"
        message += f"""\n{doc['_id']} -> {doc['count']} шт. = {doc['total']} руб.\n"""
        message += '\n'
    print("################################")
    message += "################################"
    start_time = str(datetime.now())
    time_threshold = datetime.utcnow() - timedelta(minutes=15)  # момент времени 15 минутной давности
    print(start_time)
    message += "\n За последние 15 минут: \n"
    pipeline = [
        {
            '$match': {
                'timestamp': {'$gte': time_threshold}
            }
        },
        {
            '$group': {
                '_id': '$CarWashId',
                "total": {"$sum": "$Sum"},
                'count': {'$sum': 1}
            }
        }
    ]
    for doc in col.aggregate(pipeline):
        print(doc)
        message += str(doc)
        message += '\n'
    await bot.send_message(CHANNEL_ID, message)
    print("################################")


async def main():
    await for_all_time()

    s = await bot.get_session()
    await s.close()


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
