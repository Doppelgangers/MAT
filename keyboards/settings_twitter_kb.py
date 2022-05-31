from  aiogram.types import ReplyKeyboardMarkup ,  KeyboardButton

load_twitter = KeyboardButton('Загрузить твитер аккаунты')
main_menu = KeyboardButton('Главное меню')
link_twitter_for_proxy = KeyboardButton ("Привязать к прокси")

kb_settings_twitter = ReplyKeyboardMarkup(resize_keyboard=True )

kb_settings_twitter.row(load_twitter , link_twitter_for_proxy).add(main_menu)