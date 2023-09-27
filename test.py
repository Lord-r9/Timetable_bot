from aiogram import Bot, executor, Dispatcher, types
from config import TOKEN_API


bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['auth'])
async def auth_command(message: types.Message):
    await message.reply("Для авторизации введите свою фамилию, имя и отчество в одной строке через пробел.")

@dp.message_handler(lambda message: message.text.count(' ') == 2)
async def process_name(message: types.Message):
    full_name = message.text
    await message.reply("Введите номер группы.")

@dp.message_handler()
async def process_group(message: types.Message):
    group = message.text

    # Тут можно выполнить дополнительные действия,
    # например, сохранить данные пользователя в базе данных

    await message.reply("Вы успешно авторизованы!")

if __name__ == '__main__':
    executor.start_polling(dp)
