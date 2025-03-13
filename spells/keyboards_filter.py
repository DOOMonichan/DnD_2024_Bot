from spells.edit_DataBace import get_filter_param
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

#Перевод из двоичного в булево значение параметра и вывод текста кнопки (Нажата\нет)
def checking_value(value, text_value):
    if str(value) == "1":
        text = f"✔{str(text_value)}✔"
        check = "True"
    else:
        text = str(text_value)
        check = "False"
    return text, check


#Генератор инлайн-вкладок, возвращает лист из кнопок
async def generate_keyboard_tabs_filter(user_id):
    values_param = await get_filter_param(user_id, "tabs")
    tabs = list()
    tabs_cells = types.InlineKeyboardButton(text="|Ячейки заклинаний|", callback_data=f"filter_tabs_{str(bool(int(values_param[0])))}_0")
    tabs_class = types.InlineKeyboardButton(text="|Классы|", callback_data=f"filter_tabs_{str(bool(int(values_param[1])))}_1")
    tabs_school = types.InlineKeyboardButton(text="|Школы|", callback_data=f"filter_tabs_{str(bool(int(values_param[2])))}_2")
    tabs_time = types.InlineKeyboardButton(text="|Время накладывания|", callback_data=f"filter_tabs_{str(bool(int(values_param[3])))}_3")
    tabs_distance = types.InlineKeyboardButton(text="|Дистанция накладывания|", callback_data=f"filter_tabs_{str(bool(int(values_param[4])))}_4")
    tabs_duration = types.InlineKeyboardButton(text="|Длительность заклинания|", callback_data=f"filter_tabs_{str(bool(int(values_param[5])))}_5")
    tabs_components = types.InlineKeyboardButton(text="|Компоненты заклинания|", callback_data=f"filter_tabs_{str(bool(int(values_param[6])))}_6")
    tabs = [tabs_cells, tabs_class, tabs_school, tabs_time, tabs_distance, tabs_duration, tabs_components]
    return tabs


#Сборщик инлайн клавиатуры всех фильтров
async def generate_all_keyboard_filter(user_id):
    check_tabs = await get_filter_param(user_id, "tabs")
    tabs = await generate_keyboard_tabs_filter(user_id)
    builder = InlineKeyboardBuilder()

    builder.row(tabs[0])
    if check_tabs[0] == "1":
        kb_cells = await generate_keyboard_cells_filter(user_id)
        builder.row(kb_cells[0])
        for row in kb_cells[1:]:
            builder.row(row[0])
            for button in row[1:]:
                builder.add(button)

    builder.row(tabs[1])
    if check_tabs[1] == "1":
        kb_class = await generate_keyboard_class_filter(user_id)
        for row in kb_class:
            builder.row(row[0], row[1]) 

    builder.row(tabs[2])
    if check_tabs[2] == "1":
        kb_shcool = await generate_keyboard_school_filter(user_id)
        for row in kb_shcool:
            builder.row(row[0], row[1]) 

    builder.row(tabs[3])
    if check_tabs[3] == "1":
        kb_time = await generate_keyboard_time_filter(user_id)
        builder.row(kb_time[0][0], kb_time[0][1])
        for row in kb_time[1:5]:
            builder.row(row[0])

    builder.row(tabs[4])
    if check_tabs[4] == "1":
        kb_distance = await generate_keyboard_distance_filter(user_id)
        for row in kb_distance[:2]:
            builder.row(row[0], row[1])
        for row in kb_distance[2:4]:
            builder.row(row[0])

    builder.row(tabs[5])
    if check_tabs[5] == "1":
        kb_duration = await generate_keyboard_duration_filter(user_id)
        for row in kb_duration[:2]:
            builder.row(row[0], row[1])
        for row in kb_duration[2:5]:
            builder.row(row[0])

    builder.row(tabs[6])
    if check_tabs[6] == "1":
        kb_components = await generate_keyboard_components_filter(user_id)
        builder.row(kb_components[0][0], kb_components[0][1])
        for row in kb_components[1:3]:
            builder.row(row[0])

    builder.row(types.InlineKeyboardButton(text="|Применить|", callback_data=f"finish_filter"))
    builder.row(types.InlineKeyboardButton(text="|Сбросить|", callback_data=f"reset_filter")) 
    return builder.as_markup()


#Далее идут генераторы инлайн кнопок по каждому фильтру
async def generate_keyboard_cells_filter(user_id):
    text_values = ["Заговор","1", "2", "3", "4", "5", "6", "7", "8", "9"]
    kb_cells = list()
    values = await get_filter_param(user_id, "cells")
    text, check = checking_value(values[0], text_values[0])
    kb_cells.append(types.InlineKeyboardButton(text=text, callback_data=f"filter_cells_{check}_0"))
    index = 1
    for list_i in range(1,4):
        kb_cells.append(list())
        for _ in range(3):
            text, check = checking_value(values[index], text_values[index])
            kb_cells[list_i].append(types.InlineKeyboardButton(text=text, callback_data=f"filter_cells_{check}_{str(index)}"))
            index += 1
    return kb_cells
    

async def generate_keyboard_class_filter(user_id):
    text_values =  ["Бард", "Жрец", "Следопыт", "Друид", "Колдун", "Паладин", "Чародей", "Волшебник"]
    kb_class = list()
    values = await get_filter_param(user_id, "class")
    index = 0
    for list_i in range(4):
        kb_class.append(list())
        for _ in range(2):
            text, check = checking_value(values[index], text_values[index])
            kb_class[list_i].append(types.InlineKeyboardButton(text=text, callback_data=f"filter_class_{check}_{str(index)}"))
            index += 1
    return kb_class 


async def generate_keyboard_school_filter(user_id):
    text_values =  ["Ограждение", "Вызов", "Прорицание", "Очарование", "Воплощение", "Иллюзия", "Некромантия", "Преобразование"]
    kb_school = list()
    values = await get_filter_param(user_id, "school")
    index = 0
    for list_i in range(4):
        kb_school.append(list())
        for _ in range(2):
            text, check = checking_value(values[index], text_values[index])
            kb_school[list_i].append(types.InlineKeyboardButton(text=text, callback_data=f"filter_school_{check}_{str(index)}"))
            index += 1
    return kb_school 


async def generate_keyboard_time_filter(user_id):
    text_values =  ["Реакция", "Действие", "Бонусное действие", "1 минута", "Больше минуты", "Ритуал"]
    kb_time = list()
    values = await get_filter_param(user_id, "time")
    index = 0
    kb_time.append(list())
    for _ in range(2):
        text, check = checking_value(values[index], text_values[index])
        kb_time[0].append(types.InlineKeyboardButton(text=text, callback_data=f"filter_time_{check}_{str(index)}"))
        index += 1
    for list_i in range(1, 5):
        kb_time.append(list())
        text, check = checking_value(values[index], text_values[index])
        kb_time[list_i].append(types.InlineKeyboardButton(text=text, callback_data=f"filter_time_{check}_{str(index)}"))
        index += 1
    return kb_time 


async def generate_keyboard_distance_filter(user_id):
    text_values =  ["На себя", "Касание", "до 30 фт", "30 фт", "60-119 фт", "120 фт и больше"]
    kb_distance = list()
    values = await get_filter_param(user_id, "distance")
    index = 0
    for list_i in range(2):
        kb_distance.append(list())
        for _ in range(2):
            text, check = checking_value(values[index], text_values[index])
            kb_distance[list_i].append(types.InlineKeyboardButton(text=text, callback_data=f"filter_distance_{check}_{str(index)}"))
            index += 1
    for list_i in range(2, 4):
        kb_distance.append(list())
        text, check = checking_value(values[index], text_values[index])
        kb_distance[list_i].append(types.InlineKeyboardButton(text=text, callback_data=f"filter_distance_{check}_{str(index)}"))
        index += 1
    return kb_distance 


async def generate_keyboard_duration_filter(user_id):
    text_values =  ["Мгновенно", "Раунд", "Минута", "Больше минуты", "Концентрация минуту и менее", "Концентрация больше минуты", "Пока не рассеется"]
    kb_duration = list()
    values = await get_filter_param(user_id, "duration")
    index = 0
    kb_duration.append(list())
    for list_i in range(2):
        kb_duration.append(list())
        for _ in range(2):
            text, check = checking_value(values[index], text_values[index])
            kb_duration[list_i].append(types.InlineKeyboardButton(text=text, callback_data=f"filter_duration_{check}_{str(index)}"))
            index += 1
    for list_i in range(2, 5):
        kb_duration.append(list())
        text, check = checking_value(values[index], text_values[index])
        kb_duration[list_i].append(types.InlineKeyboardButton(text=text, callback_data=f"filter_duration_{check}_{str(index)}"))
        index += 1
    return kb_duration


async def generate_keyboard_components_filter(user_id):
    text_values =  ["Вербальный", "Соматический", "Материальный не расходуемый", "Материальный расходуемый"]
    kb_components = list()
    values = await get_filter_param(user_id, "components")
    index = 0
    kb_components.append(list())
    for _ in range(2):
        text, check = checking_value(values[index], text_values[index])
        kb_components[0].append(types.InlineKeyboardButton(text=text, callback_data=f"filter_components_{check}_{str(index)}"))
        index += 1
    for list_i in range(1, 3):
        kb_components.append(list())
        text, check = checking_value(values[index], text_values[index])
        kb_components[list_i].append(types.InlineKeyboardButton(text=text, callback_data=f"filter_components_{check}_{str(index)}"))
        index += 1
    return kb_components