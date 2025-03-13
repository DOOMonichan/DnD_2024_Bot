
import logging
from spells.keyboards import *
from spells.keyboards_filter import *
from spells.edit_DataBace import *
from spells.df_editor import applying_filters
from spells.SpellsFilter import filter_update, printer_filter, print_filter
from spells.SpellsSearcher import spell_serch, res_search
from aiogram import F, Dispatcher, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)
API_TOKEN =  "TG_TOKEN"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

#Переключатель улавливателя введенных сообщений
class Form(StatesGroup):
    spell = State()

#Скрывает клавиатуру
@dp.message(Command("stop"))
async def cmd_stop(message: types.Message):
    await message.answer("Клавиатура скрыта", reply_markup=types.ReplyKeyboardRemove())



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


#Старт фильтрации, обновляет положение вкладок, выводит их и сообщение о примененых фильтрах
@dp.message(Command("filter"))
@dp.message(F.text=="Фильтровать")
async def cmd_search_filter(message: types.Message):
    user_id = message.from_user.id
    await update_filter_param(user_id, "tabs", "0000000")
    tabs = await generate_keyboard_tabs_filter(user_id)
    builder = InlineKeyboardBuilder()
    for tab in tabs:
        builder.row(tab, width=1)
    text, dict_filter = await print_filter(user_id)
    df_filter = await applying_filters(dict_filter)
    num_spells = len(df_filter["name"])
    text += f"\n_Кол-во найденых заклинаний: {num_spells}_"
    builder.row(types.InlineKeyboardButton(text="|Применить|", callback_data=f"finish_filter"))
    builder.row(types.InlineKeyboardButton(text="|Сбросить|", callback_data=f"reset_filter")) 
    await message.answer(f"*Сейчас применены такие фильтры:*\n{text}", parse_mode="Markdown", reply_markup=builder.as_markup())


#Обновление сообщения фильтра с изменением кнопок и информации о применяемых фильтрах
@dp.callback_query(F.data.startswith("filter_"))
async def filter_(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if callback.data.startswith("filter_"):
        await filter_update(callback)
    text, dict_filter = await print_filter(user_id)
    df_filter = await applying_filters(dict_filter)
    num_spells = len(df_filter["name"])
    text += f"\n_Кол-во найденых заклинаний: {num_spells}_"
    kb = await generate_all_keyboard_filter(user_id)
    chat_id=callback.message.chat.id
    message_id=callback.message.message_id
    await bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, parse_mode="Markdown")
    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=kb)


#Конец обработки фильтров, выводит найденные по запросу заклинания
@dp.callback_query(F.data.startswith("finish_filter"))
async def finish_filter(callback: types.CallbackQuery):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await printer_filter(callback)


#Сброс фильтров
@dp.callback_query(F.data.startswith("reset_filter"))
async def reset_filter(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await rec_new_filter(user_id)
    await filter_(callback)


#Переход на другую страницу в найденных по фильтру заклинаниях
@dp.callback_query(F.data.startswith("keyboard_filter_"))
async def keyboard_filter(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    index_spells =  await get_filter_param(user_id, "index_list")
    page = int(callback.data.replace("keyboard_filter_", ""))
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


 