from  aiogram.types import ReplyKeyboardMarkup ,  KeyboardButton

load_proxy = KeyboardButton('Загрузить прокси')
main_menu = KeyboardButton('Главное меню')

kb_settings_proxy = ReplyKeyboardMarkup(resize_keyboard=True )

kb_settings_proxy.add(load_proxy).add(main_menu)