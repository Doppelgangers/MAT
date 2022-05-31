from aiogram.utils import executor
from create_bot import dp
from data_base import sql_db

async def on_startup(_):
    sql_db.sql_start()
    print("Бот успешно запущен >_<")

from handlers import other , gift , load_proxy , load_twitter

other.reg_handler_other(dp)
gift.reg_handler_gift(dp)
load_proxy.reg_handler_load_proxy(dp)
load_twitter.reg_handler_load_twitter(dp)

executor.start_polling(dp ,skip_updates=True , on_startup=on_startup)