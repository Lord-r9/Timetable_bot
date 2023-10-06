from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardButton
import datetime
symb_next="➡"
symb_previous="⬅"
kb = InlineKeyboardBuilder()
kb.as_markup(resize_keyboard=True)

kb.add(InlineKeyboardButton(text=symb_previous,callback_data='-1'))
kb.add(InlineKeyboardButton(text=f"{datetime.datetime.now().strftime('%d.%m.%Y')}",callback_data='0'))
kb.add(InlineKeyboardButton(text=symb_next,callback_data='1'))