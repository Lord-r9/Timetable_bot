from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder, KeyboardButton,InlineKeyboardButton

kb = InlineKeyboardBuilder()
kb.as_markup(resize_keyboard=True)
kb.add(InlineKeyboardButton(text="Today",callback_data='1'))
kb.add(InlineKeyboardButton(text="Tomorrow",callback_data='0'))