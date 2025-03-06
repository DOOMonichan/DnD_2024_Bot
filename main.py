import asyncio
from spells.edit_DataBace import *
from handlers import *
from aiogram import F
from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    await rec_new_user(user_id, username)
    await rec_new_filter(user_id)
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начнем!"))
    await message.answer(f"Привет, {username}. Я бот созданный для удобного поиска заклинаний в PHB 2024. Пока мой функционал ограничен поиском заклинаний и добавлением их в избранное.", reply_markup=builder.as_markup(resize_keyboard=True))


async def main():
    await create_table_favourites_spells()
    await create_table_filter_spells()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())     