from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import datetime

bd = ReplyKeyboardBuilder()
bd.row(KeyboardButton(text='Расписание 📖'))
bd.row(
    KeyboardButton(text='Погода 🌨'),
    KeyboardButton(text='Курс 💹')
)
bd.row(KeyboardButton(text='Авторизация 🌏'))

val = InlineKeyboardBuilder()
val.as_markup(resize_keyboard=True)
val.add(InlineKeyboardButton(text='USD💵', callback_data='USD'))
val.add(InlineKeyboardButton(text='EUR💶', callback_data='EUR'))
val.row(
    InlineKeyboardButton(text='JPY💴', callback_data='JPY'),
    InlineKeyboardButton(text='CNY💰', callback_data='CNY')
)

symb_next="➡"
symb_previous="⬅"
kb = InlineKeyboardBuilder()
kb.as_markup(resize_keyboard=True)

kb.add(InlineKeyboardButton(text=symb_previous,callback_data='-1'))
kb.add(InlineKeyboardButton(text=f"{datetime.datetime.now().strftime('%d.%m.%Y')}",callback_data='0'))
kb.add(InlineKeyboardButton(text=symb_next,callback_data='1'))