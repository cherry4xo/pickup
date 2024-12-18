import time
import asyncio

from tortoise import run_async
from telebot.asyncio_filters import StateFilter

from app.db.init_db import init, create_default_admin_user
# from app.editing.handlers import send_rounded
from app.editing.handler import send_rounded

from app.bot.handler import bot


if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    run_async(init())
    run_async(create_default_admin_user())
    while True:
        try:
            loop = asyncio.get_event_loop()
            f1 = loop.create_task(bot.polling(none_stop=True))
            f2 = loop.create_task(send_rounded())
            loop.run_forever()
        except Exception as e:
            delay = 3
            text = f'Error: {e.with_traceback()}, restarting after {delay} seconds'
            print(text)
            time.sleep(delay)
            text = f'Restarted'
            print(text)