import asyncio

from aiogram import Bot, Dispatcher, types, F
import config
from keyboards import kb
from aiogram.filters import Command, CommandStart

from DB import DB
from UnnSession import UnnSession
from TableParser import TableParser

bot = Bot(config.TOKEN_API)
dp = Dispatcher()
db = DB()
unn = UnnSession()
tp = TableParser()


@dp.message(Command(commands='start'))
async def cmd_start(message: types.Message):
    await message.answer(f'{message.from_user.first_name}, добро пожаловать!')
    await message.delete()


@dp.message(Command(commands='auth'))
async def auth_command(message: types.Message):
    await message.reply('Для авторизации введите свою фамилию, имя и отчество в одной строке через пробел.')


@dp.message(F.text.regexp(r'([а-яА-Яa-zA-z]+ )([а-яА-Яa-zA-z]+)( [а-яА-Яa-zA-z]*)?'))
async def process_name(message: types.Message):
    db.add_user_name(message.chat.id, message.text)
    await message.reply('Теперь введите номер группы.')


@dp.message(lambda message: message.text[0].isdigit())
async def process_group(message: types.Message):
    db.add_group_number(message.chat.id, message.text)
    info = db.get_user_info(message.chat.id)
    await message.reply(f'Вы успешно авторизованы!\n\nФИО: {info[0]}\nГруппа: {info[1]}')


@dp.message(Command('schedule'))
async def schedule_command(message: types.Message):
    await message.answer(text='Ваше расписание...', reply_markup=kb.as_markup())


@dp.callback_query()
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
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
