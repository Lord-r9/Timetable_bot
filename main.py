import asyncio
import config

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import kb

from DB import DB
from UnnSession import UnnSession
from TableParser import TableParser

router = Router()

db = DB()
unn = UnnSession()
tp = TableParser()

class Form(StatesGroup):
    chat_id = State()
    name = State()
    group_number = State()

@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f'{message.from_user.first_name}, добро пожаловать!')
    await message.delete()

@router.message(Command('auth'))
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


@router.message(Command('schedule'))
async def schedule_command(message: types.Message):
    await message.answer(text='Ваше расписание...', reply_markup=kb.as_markup())


@router.callback_query()
async def timetable(callback: types.CallbackQuery):
    date = callback.data
    try:
        date = int(date)
    except:
        await callback.message.answer("Не удалось получить расписание")
    if 0 > date < 15:
        await callback.message.answer("Неправильная дата")
    name, group = db.get_user_info(callback.message.chat.id)
    timetable = tp.parse(unn.get_table(name, group, date))
    table = f"{unn.get_time(date)}\n"
    for lesson in timetable['lessons']:
        if lesson['date'] == unn.get_time(date):
            table += f'({lesson["beginLesson"]}:{lesson["endLesson"]}) *{lesson["discipline"]}* ({lesson["building"]} аудитория:{lesson["auditorium"]}) \n'
    await callback.message.edit_text(text=table, reply_markup=kb.as_markup(),parse_mode='markdown')


async def main():
    bot = Bot(config.TOKEN_API)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
