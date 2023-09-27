from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder, KeyboardButton

kb = ReplyKeyboardBuilder()
kb.add(KeyboardButton(text="Today",))
kb.add(KeyboardButton(text="Tomorrow"))