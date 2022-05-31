from  aiogram.types import ReplyKeyboardMarkup ,  KeyboardButton

b1 = KeyboardButton('Ретвит поста')
b2 = KeyboardButton('Лайкнуть пост')
b3 = KeyboardButton('Отметить друзей')
b4 = KeyboardButton('Подписаться')
b5 = KeyboardButton('Активность')



kb_actions = ReplyKeyboardMarkup(resize_keyboard=True )

kb_actions.row(b1,b2,b3,b4).add(b5)