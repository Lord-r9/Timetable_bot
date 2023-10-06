import asyncio
import config
import datetime

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from DB import DB
from UnnSession import UnnSession
from TableParser import TableParser

from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards import kb
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
    await message.delete()

@router.callback_query()
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
            table = '\U0001F40D \n'
            for lesson in timetable:
                time = f'*{lesson["beginLesson"]}:{lesson["endLesson"]}*'
                discipline = f'{lesson["discipline"][:20]}'
                kind = f'{lesson["kindOfWork"].split()[0][:4]}'
                place = f'{lesson["building"]} : {lesson["auditorium"]}\n'
                table += (time + '|' + \
                      discipline.center(int(20-len(discipline))) + '|' + \
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
