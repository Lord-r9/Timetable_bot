from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         one_time_keyboard=True)
a = KeyboardButton(text="Today")
b = KeyboardButton(text="Tomorrow")
kb.add(a).add(b)
