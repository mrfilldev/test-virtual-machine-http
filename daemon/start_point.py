import asyncio

from dotenv import load_dotenv
import daemon
load_dotenv()


async def main():
    order = await daemon.get_order_messege_queue()
    #daemon.write_into_db(order)

    print("FINISHED")


if __name__ == '__main__':
    print("RUNNING")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    loop.close()
    print("FINISHED")
