from aiogram import types , Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State , StatesGroup

from create_bot import bot
from data_base import sql_db
from keyboards import kb_close  , kb_settings_twitter

class FSM_load_twiter(StatesGroup):
    twitter_list = State()

#Запросим файл
async def add_twitter (mesage : types.Message ):
    await FSM_load_twiter.twitter_list.set()
    await bot.send_message(mesage.chat.id , "Загрузити файл с твиттер аккаунтами: " , reply_markup=kb_close)


# Сохраним ссылку и запросим следующий параметр
async def load_twitters(mesage: types.Message, state: FSMContext):
    good_twitter = 0
    bed_twitter = 0
    bed_list = []
    query = []

    file = await bot.get_file(mesage.document.file_id)
    download_file = await bot.download_file(file.file_path)
    print("Пользователь загрузил файл с твитами")
    try:
        # Получаем текст из загруженного файла
        text = download_file.read().decode()
        # Удаляем лишние пробелы , удаляем символы \r , и дедаем массив из каждой строки
        twits = text.strip().replace("\r", "").split('\n')

        for twit in twits:
            username ,password , mail = twit.split(':')
            if  ( twit.count(':') == 2 and ( mail.isdigit() or mail.count('@') or mail.count('+')  ) ):
                good_twitter += 1
                query.append( [username ,password , mail] )
            else:
                bed_twitter += 1
                bed_list.append(twit)

        try:
            await sql_db.set_twitter(query)
        except:
            await bot.send_message(mesage.chat.id, "Во время загрузки файла произашла ошибка")
            return

        answere = f"Успешно загруженно {good_twitter} твиттер аккаунт(ов).\n\n"

        if bed_twitter > 0:
            answere += f'Неудалось загрузить {bed_twitter} твиттер аккаунт(ов).\n'
            answere += '\n'.join(bed_list)

        await bot.send_message(mesage.chat.id, answere, reply_markup=kb_settings_twitter)
        await state.finish()
    except:
        await bot.send_message(mesage.chat.id, "Это не похоже на файл с твиттер аккаунтами")


def reg_handler_load_twitter(dp : Dispatcher ):
    dp.register_message_handler(add_twitter , Text(equals="Загрузить твитер аккаунты" , ignore_case=True), state=None)
    dp.register_message_handler(load_twitters , content_types=['document'], state=FSM_load_twiter.twitter_list)

