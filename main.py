from aiogram import Bot, executor, Dispatcher, types
from config import TOKEN_API
from keyboards import kb


bot = Bot(TOKEN _API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'{message.from_user.first_name}, добро пожаловать!')

@dp.message_handler(commands=['auth'])
async def auth_command(message: types.Message):
    await message.reply('Для авторизации введите свою фамилию, имя и отчество в одной строке через пробел.')
@dp.message_handler(lambda message: message.text.count(' ') == 2)
async def process_name(message: types.Message):
    global full_name
    full_name = message.text
    await message.reply('Теперь введите номер группы.')

@dp.message_handler(lambda message: message.text[0].isdigit())
async def process_group(message: types.Message):
    global group
    group = message.text
    await message.reply(f'Вы успешно авторизованы!\n\nФИО: {full_name}\nГруппа: {group}')

@dp.message_handler(commands=['schedule'])
async def schedule_command(message: types.Message):
    await message.answer(text='Ваше расписание...', reply_markup=kb)
    # парсер для получения расписания
    #schedule = parser_function()

    #if schedule:
    #   await message.reply("Вот ваше расписание:")
    #    await message.reply(schedule)
    #else:
    #    await message.reply("К сожалению, не удалось получить расписание.")


if __name__ == '__main__':
    executor.start_polling(dp)
