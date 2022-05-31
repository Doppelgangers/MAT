from  aiogram.types import ReplyKeyboardMarkup ,  KeyboardButton

proxy_list = KeyboardButton('Настройка прокси')
twitter_list = KeyboardButton('Настройка твиттер аккаунтов')
profile_list = KeyboardButton('Настройка профилей')
activity_list = KeyboardButton('Активность')
kb_main_menu = ReplyKeyboardMarkup(resize_keyboard=True )

kb_main_menu.row(proxy_list ,twitter_list).row(profile_list , activity_list)