import asyncio
from aiogram import Bot, types
from dotenv import load_dotenv
import os

load_dotenv()



CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
bot = Bot(token=os.getenv('BOT_TOKEN'))


async def main():
    await bot.send_message(CHANNEL_ID, 'Теперь я буду учиться отправлять сюда сообщения со статистикой о тестовых заказах!')
    s = await bot.get_session()
    await s.close()


if __name__ == '__main__':
    print("RUNNING")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    loop.close()
    print("FINISHED")

# async def send_message(channel_id: int, text: str):
#     await bot.send_message(channel_id, text)
# executor.start_webhook(dp, skip_updates=True)
# executor.start_polling(dp, skip_updates=True)
"""
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    # logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    # logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
"""
# # webhook settings
# WEBHOOK_HOST = 'https://test-tanker-carwash.ru/'
# WEBHOOK_PATH = ''
# WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
#
# WEBAPP_HOST = '127.0.0.1'
# WEBAPP_PORT = 8081
