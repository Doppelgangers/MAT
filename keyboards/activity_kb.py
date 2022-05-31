from  aiogram.types import ReplyKeyboardMarkup ,  KeyboardButton

actions = KeyboardButton('Дейстивя')
go_to_giv = KeyboardButton('Учавствовать в гиве')
main_menu = KeyboardButton('Главное меню')

kb_activity = ReplyKeyboardMarkup(resize_keyboard=True )

kb_activity.row(actions , go_to_giv ).add(main_menu)