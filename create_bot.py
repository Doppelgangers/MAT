from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

TOKEN = '1219818658:AAERsK7cI_NPgqPz8naLk1EuS8822FtyudM'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot , storage=storage)