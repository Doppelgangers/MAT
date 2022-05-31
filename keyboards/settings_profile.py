from  aiogram.types import ReplyKeyboardMarkup ,  KeyboardButton

ava = KeyboardButton('Изменить автораку')
name = KeyboardButton('Изменить имя')
bacground = KeyboardButton('Изменить фон')
tag = KeyboardButton('Изменить тег')
biography = KeyboardButton('Изменить биографию')
main_menu = KeyboardButton('Главное меню')

kb_settings_profile = ReplyKeyboardMarkup(resize_keyboard=True )

kb_settings_profile.row(ava , name , bacground ,tag ,biography).add(main_menu)