from  aiogram.types import ReplyKeyboardMarkup ,  KeyboardButton

cls = KeyboardButton('/отмена')

kb_close = ReplyKeyboardMarkup(resize_keyboard=True )

kb_close.add(cls)