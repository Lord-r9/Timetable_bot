import asyncio
import config
import datetime
import requests
import json


from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from DB import DB
from UnnSession import UnnSession
from TableParser import TableParser

from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards import kb, bd, val
from keyboards import symb_previous, symb_next

router = Router()
db = DB()
unn = UnnSession()
tp = TableParser()
bot = Bot(config.TOKEN_API)
dp = Dispatcher()
dp.include_router(router)

class Form(StatesGroup):
    name = State()
    group_number = State()
    val = State()
    shcudle = State()

@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f'{message.from_user.first_name}, добро пожаловать!', reply_markup=bd.as_markup(resize_keyboard=True))
    await message.delete()

@router.message(F.text == 'Авторизация 🌏')
async def auth_command(message: types.Message, state: FSMContext):
    await message.reply('Для авторизации введите свою фамилию, имя и отчество в одной строке через пробел.')
    await state.set_state(Form.name)

@router.message(Form.name, F.text.regexp(r'([А-ЯЁ][а-яё]+[\-\s]?){3,}'))
async def process_name(message: types.Message, state: FSMContext):
    db.add_user_name(message.chat.id, message.text)
    await message.reply('Теперь введите номер группы.')
    await state.set_state(Form.group_number)

@router.message(Form.name)
async def process_name_check(message: types.Message):
    await message.reply('Проверьте правильность введенных данных')

@router.message(Form.group_number, lambda message: message.text[0].isdigit())
async def process_group(message: types.Message, state: FSMContext):
    db.add_group_number(message.chat.id, message.text)
    info = db.get_user_info(message.chat.id)
    await message.reply(f'Вы успешно авторизованы!\n\nФИО: {info[0]}\nГруппа: {info[1]}')
    await state.clear()

@router.message(Form.group_number)
async def process_group_check(message: types.Message):
    await message.reply('Номер группы должен состоять из цифр и/или букв')


@router.message(F.text == 'Расписание 📖')
async def schedule_command(message: types.Message, state: FSMContext):
    await message.answer(text='Ваше расписание...', reply_markup=kb.as_markup())
    await state.set_state(Form.shcudle)

@router.message(F.text == 'Курс 💹')
async def schedule_command(message: types.Message, state: FSMContext):
    await message.answer(text='Выберете валюту', reply_markup=val.as_markup())
    await state.set_state(Form.val)

@router.callback_query(Form.val)
async def timetable(callback: types.CallbackQuery):
    data = requests.get(config.URL_val).json()
    currency = str(callback.data)
    await callback.message.edit_text(text=str(data['Valute'][currency]['Value']/data['Valute'][currency]['Nominal']) + ' ₽')
    await callback.message.edit_reply_markup(reply_markup=val.as_markup())


@router.message(F.text == 'Погода 🌨')
async def schedule_command(message: types.Message):
    weather_data = requests.get(config.URL).json()

    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])
    wind_speed = round(weather_data['wind']['speed'])
    humidity = round(weather_data['main']['humidity'])
    await message.answer(text=f'Сейчас в Нижнем Новгороде {str(temperature)} °C \n'
                              f'Ощущается как {str(temperature_feels)} °C \n'
                              f'Скорость ветра {str(wind_speed)} м/с \n'
                              f'Влажность {str(humidity)} %')


emoji = {'07:30': '1️⃣', '09:10': '2️⃣', '10:50': '3️⃣', '13:00': '4️⃣', '14:40': '5️⃣', '16:20': '6️⃣', '18:00': '7️⃣'}

@router.callback_query(Form.shcudle)
async def timetable(callback: types.CallbackQuery):
    date = int(callback.data)
    new_kb = InlineKeyboardBuilder()
    if date > -15:
        new_kb.button(text=symb_previous, callback_data=str(date - 1))
    new_kb.button(text=f"{(datetime.datetime.now() + datetime.timedelta(days=date)).strftime('%d.%m.%Y')}",
                  callback_data=str(date))
    if date < 15:
        new_kb.button(text=symb_next, callback_data=str(date + 1))
    try:
        name, group = db.get_user_info(callback.message.chat.id)
    except TypeError:
        await callback.message.edit_text(text='Для начала необходимо авторизоваться')
    else:
        async with ChatActionSender.typing(bot=bot, chat_id=callback.message.chat.id):
            timetable = tp.parse(unn.get_table(name, group, date=date))
            table = '🐍 \n'
            for lesson in timetable:
                time = f' *{lesson["beginLesson"]}-{lesson["endLesson"]}* '
                discipline = f' {lesson["discipline"][:20]} '
                kind = f' {lesson["kindOfWork"].split()[0][:4]} '
                lect = lesson["lecturer"].split()
                if len(lect) == 3:
                    lect_correct = f' {lect[0]} {lect[1][0]}.{lect[2][0]}. '
                else:
                    lect_correct = f' '
                place = f' *{lesson["building"]} : {lesson["auditorium"]}*   \n'
                table += (emoji[lesson["beginLesson"]] + time + '|' + \
                      discipline + '|' + \
                      kind + '|' + \
                      lect_correct + '|' + \
                      place.replace("Корпус", "Кор.").replace("Виртуальное", "Дист.")
                      )
            if table != callback.message.text:
                await callback.message.edit_text(text=str(table), parse_mode='markdown')
                await callback.message.edit_reply_markup(reply_markup=new_kb.as_markup())


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
