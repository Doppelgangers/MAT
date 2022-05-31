from aiogram import types, Dispatcher
from create_bot import bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import kb_close, kb_settings_proxy, kb_main_menu

from data_base import sql_db


class FSM_load_proxy(StatesGroup):
    proxy_list = State()


# Запросим файл
async def add_proxy(mesage: types.Message):
    await FSM_load_proxy.proxy_list.set()
    await bot.send_message(mesage.chat.id, "Загрузити файл с прокси: ", reply_markup=kb_close)


# Сохраним ссылку и запросим следующий параметр
async def load_proxy(mesage: types.Message, state: FSMContext):
    good_proxy = 0
    bed_proxy = 0
    exists_proxy = 0
    bed_list = []

    file = await bot.get_file(mesage.document.file_id)
    download_file = await bot.download_file(file.file_path)
    print("Пользователь загрузил файл прокси")
    try:
        # Получаем текст из загруженного файла
        text = download_file.read().decode()
        # Удаляем лишние пробелы , удаляем символы \r , и дедаем массив из каждой строки
        lists = text.strip().replace("\r", "").split('\n')
        for line in lists:
            aut, prox = line.split('@')
            log, pas = aut.split(':')
            ip, port = prox.split(':')
            if ip.count(".") == 3 and port.isdigit():

                added = await sql_db.set_proxy(log, pas, ip, port)

                if added:
                    print('Добавил адрес', ip, port, log, pas)
                    good_proxy += 1
                else:
                    print('Повторное значение', ip, port, log, pas)
                    exists_proxy += 1

            else:
                bed_proxy += 1
                bed_list.append(line)
                print('Несмог загрузить ', line)

        answere = f"Успешно загруженно {good_proxy} прокси.\n\n"

        if exists_proxy > 0:
            answere += f'Ранее добавленные прокси: {exists_proxy} \n\n'

        if bed_proxy > 0:
            answere += f'Неудалось загрузить {bed_proxy} прокси.\n'
            answere += '\n'.join(bed_list)

        await bot.send_message(mesage.chat.id, answere, reply_markup=kb_settings_proxy)
        await state.finish()

    except:
        await bot.send_message(mesage.chat.id, "Это не похоже на файл  с прокси")





def reg_handler_load_proxy(dp: Dispatcher):
    dp.register_message_handler(add_proxy, Text(equals="Загрузить прокси", ignore_case=True), state=None)
    dp.register_message_handler(load_proxy, content_types=['document'], state=FSM_load_proxy.proxy_list)
