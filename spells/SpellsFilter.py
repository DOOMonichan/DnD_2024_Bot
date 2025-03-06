import pandas as pd
from spells.edit_DataBace import get_filter_param, update_filter_param
from spells.keyboards import generate_filter_keyboard, filtered_spell_generator_keyboard
from aiogram import types
from spells.df_editor import spell_names, applying_filters


#Обновление значения конкретного параметра и вызов генератора клавиатуры с тем же параметром
async def filter_update(callback: types.CallbackQuery) -> None:
    param, value, index_param = callback.data.split("_")[1:]
    index_param = int(index_param)
    user_id = callback.from_user.id
    value_param =  await get_filter_param(user_id, param)
    if value == "True":
        value_param = value_param[:index_param] + "1" + value_param[index_param+1:]
    else:
        value_param = value_param[:index_param] + "0" + value_param[index_param+1:]
    await update_filter_param(user_id, param, value_param)
    kb = await generate_filter_keyboard(value_param, param)
    return kb


#Когда нажата кнопка продолжить. 
async def finish_filter(callback: types.CallbackQuery) -> None:
    param = callback.data.split("_")[-1]
    list_param = ["cells", "class", "school", "time", "distance", "components", "duration"]
    list_text = ["Выберете ячейки заклинаний", "Выберете классы", "Выберете школы", "Выберете время накладывания", "Выберете дистанцию накладывания", "Выберете нужные компоненты", "Выберете длительность заклинания"]
    user_id = callback.from_user.id
    #Проверка кончились ли параметры, если да, то выводим список фильтров, применяем все фильтры и создаем клавиатуру с найдеными заклинаниями
    if list_param.index(param) + 1 == len(list_param):
        text, dict_filter = await print_filter(user_id)
        df_filter = await applying_filters(dict_filter)
        list_filter_spells = df_filter["name"].tolist()
        index_spells = ""
        for name in list_filter_spells:
            index_spells += f"{spell_names.index(name)},"
        index_spells = index_spells[:-1]
        await update_filter_param(user_id, "index_list", index_spells)
        num_spells = len(list_filter_spells)
        text += f"\n_Кол-во найденых заклинаний: {num_spells}_"
        kb = await filtered_spell_generator_keyboard(index_spells, 1)       
        await callback.message.answer(text, parse_mode="Markdown", reply_markup=kb)
    #Если нет то генерируем след. клавиатуру.
    else:
        index_param = list_param.index(param) + 1
        param = list_param[index_param]
        value_param = await get_filter_param(user_id, param)
        kb = await generate_filter_keyboard(value_param, param)
        await callback.message.answer(list_text[index_param], reply_markup=kb)


#Вывод всех примененых фильтров и запись их в dict_filter для дальнейшей обработки
async def print_filter(user_id):
    text = "_Фильтры применены_"
    dict_values = {"cells": ["\n*Ячейки заклинаний: *",["Заговор","1", "2", "3", "4", "5", "6", "7", "8", "9"]],
                   "class": ["\n*Классы: *", ["Варвар", "Бард", "Жрец", "Следопыт", "Друид", "Воин", "Колдун", "Плут", "Монах", "Паладин", "Чародей", "Волшебник"]],
                   "school": ["\n*Школы: *", ["Ограждение", "Вызов", "Прорицание", "Очарование", "Воплощение", "Иллюзия", "Некромантия", "Преобразование"]],
                   "time": ["\n*Время накладывания: *", ["Реакция", "Действие", "Бонусное действие", "1 минута", "Больше минуты", "Ритуал"]],
                   "distance": ["\n*Дистанцию накладывания: *", ["На себя", "Касание", "до 30 фт", "30 фт", "60-119 фт", "120 фт и больше"]],
                   "components": ["\n*Нужные компоненты: *", ["Вербальный", "Соматический", "Материальный не расходуемый", "Материальный расходуемый"]],
                   "duration": ["\n*Длительность заклинания: *", ["Мгновенно", "Раунд", "Минута", "Больше минуты", "Концентрация минуту и менее", "Концентрация больше минуты", "Пока не рассеется"]]
                   }
    dict_filter = {"cells": list(), "class": list(), "school": list(), "time": list() ,"distance": list(), "components": list(), "duration": list()}
    for param, values in dict_values.items():
        values_param = await get_filter_param(user_id, param)
        if "0" not in values_param or "1" not in values_param:
            dict_filter[param] = values[1][:]
            text += values[0] + "Все"
        else:
            text += values[0]
            for i in range(len(values_param)):
                if  values_param[i] == "1":
                    dict_filter[param].append(values[1][i])
                    text += values[1][i] + ", "
            text = text[:-2]
    return text, dict_filter





