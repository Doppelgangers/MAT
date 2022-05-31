from aiogram import types , Dispatcher
from  create_bot import  dp , bot
from aiogram.dispatcher.filters import Text
from keyboards import kb_close , kb_activity , kb_main_menu


from  aiogram.dispatcher import FSMContext
from  aiogram.dispatcher.filters.state import State , StatesGroup

from data_base import sql_db

class FSM_gift(StatesGroup):
    link = State()
    tags = State()
    mesage = State()


#Запросим ссылку
async def create_gift (mesage : types.Message ):
    await FSM_gift.link.set()
    await bot.send_message(mesage.chat.id , "Введи ссылку на гифт: " , reply_markup=kb_close)


#Сохраним ссылку и запросим следующий параметр
async def load_link(mesage : types.Message , state:FSMContext):
    async with state.proxy() as data:
        data["link"] = str(mesage.text)
        await FSM_gift.next()
        await bot.send_message(mesage.chat.id, "Введите количеаство тегов: ")


async def load_tag(mesage : types.Message , state:FSMContext):
    async with state.proxy() as data:
        data["tags"] = str(mesage.text)
        await FSM_gift.next()
        await bot.send_message(mesage.chat.id, "Введите сообщение (если не нужно введите 0): ")


async def load_mesage(mesage : types.Message , state:FSMContext):
    async with state.proxy() as data:
        data["mesage"] = str(mesage.text)

    async with state.proxy() as data:

        mes = f"Учайтие в гиве успешно созданно! \n\n {data['link']} \n\n Количество тегов: {data['tags']} \n\n "
        if data['mesage'] == '0':
            mes += 'Дополнительного сообщения нет'
        else:
            mes += f'Дополнительное сообщение: {data["mesage"]}'
        await bot.send_message(mesage.chat.id, mes , reply_markup=kb_activity)

    await state.finish()




def reg_handler_gift(dp : Dispatcher ):

    dp.register_message_handler(create_gift , Text(equals="Учавствовать в гиве" , ignore_case=True)  , state=None)
    dp.register_message_handler(load_link , state=FSM_gift.link  )
    dp.register_message_handler(load_tag , state=FSM_gift.tags  )
    dp.register_message_handler(load_mesage , state=FSM_gift.mesage  )
