from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from data_base import sql_db
from create_bot import dp, bot
from keyboards import kb_main_menu , kb_activity , kb_actions,kb_settings_proxy, kb_settings_twitter, kb_settings_profile


async def commands_start (mesage : types.Message):
    await bot.send_message( mesage.chat.id , "Добро пожаловать в MAT \n\nЭто бот Мульти Аккаунт Твитер Бот. \n Он вам позволит совершать подписки и ставить лайки на разные посты, с соти твитер аккаунтов что вы загрузили ранее." ,reply_markup=kb_main_menu )

async def activity (mesage : types.Message):
    await bot.send_message( mesage.chat.id , "Создаём активность. Выберите действие" ,reply_markup=kb_activity )

async def actions (mesage : types.Message):
    await bot.send_message( mesage.chat.id , "Выберите действия." ,reply_markup=kb_actions )

async def main_menu (mesage : types.Message):
    await bot.send_message( mesage.chat.id , "Ну вот вы и главном меню, выберети раздел что вас интересует." , reply_markup=kb_main_menu )



async def cancel_handler(mesage: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await bot.send_message(mesage.chat.id, "Вы не находитель в машинном состоянии, возврат в главное меню", reply_markup=kb_main_menu)
        return
    await state.finish()
    await bot.send_message(mesage.chat.id, "Операция прокси была прервана", reply_markup=kb_main_menu)



async def settings_proxy (mesage : types.Message):
    text = f"Настраиваем ваши прокси.\n\n"
    prx = await sql_db.get_count_proxys()
    text += f'На вашем аккаунте {str(prx)} прокси\n\nЧто хотите сделать?'

    await bot.send_message( mesage.chat.id , text , reply_markup=kb_settings_proxy )

async def settings_twitter (mesage : types.Message):
    text = f"Настраиваем ваши твиттер аккаунты.\n\n"
    prx = await sql_db.get_count_twitters()
    text += f'На вашем аккаунте {str(prx)} твиттер аккаунт(ов)\n\nЧто хотите сделать?'

    await bot.send_message( mesage.chat.id , text , reply_markup=kb_settings_twitter )

async def settings_profile (mesage : types.Message):
    text = f"Настраиваем ваши профили.\n\nЧто хотите сделать?"
    await bot.send_message( mesage.chat.id , text , reply_markup=kb_settings_profile )



def reg_handler_other(dp : Dispatcher ):
    dp.register_message_handler(cancel_handler , state="*" , commands='отмена' )
    dp.register_message_handler(cancel_handler  , Text(equals="отмена" , ignore_case=True) , state="*"  )
    dp.register_message_handler(commands_start , Text(equals='/start' , ignore_case=True))
    dp.register_message_handler(main_menu , Text(equals='Главное меню' , ignore_case=True))
    dp.register_message_handler(activity ,Text(equals='Активность' , ignore_case=True) )
    dp.register_message_handler(actions ,Text(equals='Дейстивя' , ignore_case=True) )
    dp.register_message_handler(settings_proxy ,Text(equals='Настройка прокси' , ignore_case=True) )
    dp.register_message_handler(settings_twitter ,Text(equals='Настройка твиттер аккаунтов' , ignore_case=True) )
    dp.register_message_handler(settings_profile ,Text(equals='Настройка профилей' , ignore_case=True) )