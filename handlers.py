
import logging
from spells.keyboards import *
from spells.edit_DataBace import *
from spells.SpellsFilter import filter_update, finish_filter
from spells.SpellsSearcher import spell_serch, res_search
from aiogram import F, Dispatcher, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)
API_TOKEN = "TG_TOKEN"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

#Переключатель улавливателя введенных сообщений
class Form(StatesGroup):
    spell = State()


@dp.message(F.text=="В меню")
@dp.message(F.text=="Начнем!")
async def cmd_menu(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Искать заклинание"))
    builder.add(types.KeyboardButton(text="Избранные заклинания"))
    builder.row(types.KeyboardButton(text="Поддержать проект"))
    await message.answer("Что будем кастовать?", reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(F.text=="Поддержать проект")
async def cmd_suport_project(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="100 рублей", url="https://yoomoney.ru/quickpay/confirm.xml?receiver=4100119028400777&quickpay-form=shop&targets=Sponsor%20this%20project&paymentType=SB&sum=100"))
    builder.add(types.InlineKeyboardButton(text="500 рублей", url="https://yoomoney.ru/quickpay/confirm.xml?receiver=4100119028400777&quickpay-form=shop&targets=Sponsor%20this%20project&paymentType=SB&sum=500"))
    builder.add(types.InlineKeyboardButton(text="1000 рублей", url="https://yoomoney.ru/quickpay/confirm.xml?receiver=4100119028400777&quickpay-form=shop&targets=Sponsor%20this%20project&paymentType=SB&sum=1000"))
    await message.answer("Выберите сумму", reply_markup=builder.as_markup())


@dp.message(F.text=="Искать заклинание")
async def cmd_search_spell(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Фильтровать"))
    builder.add(types.KeyboardButton(text="Поиск по названию"))
    builder.row(types.KeyboardButton(text="В меню"))
    await message.answer("Как будем искать? ", reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(Command("filter"))
@dp.message(F.text=="Фильтровать")
async def cmd_search_filter(message: types.Message):
    user_id = message.from_user.id
    param = "cells"
    param_value = str(await get_filter_param(user_id, param))
    kb = await generate_filter_keyboard(param_value, param)  
    await message.answer("Выберете ячейки заклинаний", reply_markup=kb)


@dp.callback_query(F.data.startswith("filter_"))
async def filter_(callback: types.CallbackQuery):
    kb = await filter_update(callback)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=kb)


@dp.callback_query(F.data.startswith("finish_"))
async def finish_(callback: types.CallbackQuery):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await finish_filter(callback)


@dp.callback_query(F.data.startswith("keyboard_filter_"))
async def keyboard_filter(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    page = int(callback.data.split("_")[-1])
    index_spells = await get_filter_param(user_id, "index_list")
    kb = await filtered_spell_generator_keyboard(index_spells, page)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=kb)


@dp.message(F.text=="Поиск по названию")
async def cmd_name_search(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    await state.set_state(Form.spell)
    await message.answer("Как называется искомое заклинание?", reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True))


@dp.callback_query(F.data.endswith("_spell_seeker"))
async def seeker_handler(callback: types.CallbackQuery) -> None:
    result, kb = await spell_serch(callback)
    await callback.message.answer(result, parse_mode="Markdown", reply_markup=kb)


@dp.callback_query(F.data.endswith("_spell"))
async def spell_handler(callback: types.CallbackQuery) -> None:
    text, kb = await edit_add_del_keyboard(callback)  

    await callback.answer(text)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=kb)


@dp.message(F.text=="Избранные заклинания")
async def favourites_spells(message: types.Message):
    text, kb = await generate_favourites_keyboard(message)
    await message.answer(text, reply_markup=kb)


@dp.message(Form.spell)
async def process_message(message: types.Message, state: FSMContext):
    result, kb = await res_search(message)
    await state.clear()
    await message.answer(result, parse_mode="Markdown", reply_markup=kb)


 