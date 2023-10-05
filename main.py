import asyncio

vowel = "ёуеыаоэяию"

# for keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards import symb_previous, symb_next
import datetime
from config import MAX_DATE

# for ???
from aiogram.utils.chat_action import ChatActionSender
from aiogram import Bot, Dispatcher, types, F
import config
from keyboards import kb
from aiogram.filters import Command, CommandStart

# for take info
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


def consonant(s):
    ind = 0
    for i in s:
        if i not in vowel:
            ind += 1
    return ind


@dp.callback_query()
async def timetable(callback: types.CallbackQuery):
    date = int(callback.data)

    new_kb = InlineKeyboardBuilder()
    if date > -MAX_DATE:
        new_kb.button(text=symb_previous, callback_data=str(date - 1))
    new_kb.button(text=f"{(datetime.datetime.now() + datetime.timedelta(days=date)).strftime('%d.%m.%Y')}",
                  callback_data=str(date))
    if date < MAX_DATE:
        new_kb.button(text=symb_next, callback_data=str(date + 1))

    name, group = db.get_user_info(callback.message.chat.id)
    async with ChatActionSender.typing(bot=bot, chat_id=callback.message.chat.id):
        timetable = tp.parse(unn.get_table(name, group, date=date))
        date = f"{unn.get_time(date)}\n"
        table = date
        MAX_DISCIPLINE_SIZE = 20
        MAX_KIND_SIZE = 10
        MAX_STR_SIZE=80
        for lesson in timetable:
            time = f'*{lesson["beginLesson"]}:{lesson["endLesson"]}*'
            discipline = f'{lesson["discipline"][:MAX_DISCIPLINE_SIZE]}'
            kind = f'{lesson["kindOfWork"].split()[0][:4]}'
            place = f'{lesson["building"]} : {lesson["auditorium"]}\n'
            table += (time + '|' + \
                      discipline.center(int(MAX_DISCIPLINE_SIZE-len(discipline))) + '|' + \
                      kind + '|' + \
                      place.replace("Корпус", "Кор.").replace("Виртуальное", "Дист.")
                      )
        if table != callback.message.text:
            await callback.message.edit_text(text=str(table), parse_mode='markdown')
            await callback.message.edit_reply_markup(reply_markup=new_kb.as_markup())


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
