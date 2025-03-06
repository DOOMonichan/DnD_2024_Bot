from spells.keyboards import generate_add_del_keyboard
from spells.edit_DataBace import *
import pandas as pd
from spells.df_editor import spells_data, spell_names

#Вывод описания конкретного заклинания
async def spell_serch(callback):
    index_spell = callback.data.replace("_spell_seeker", "")
    result = await spell_printer(index_spell)
    favourites_list = await get_favourites_spells_index(callback.from_user.id)
    kb = generate_add_del_keyboard(index_spell, favourites_list)
    return result, kb


#Сборщик текста заклинания
async def spell_printer(index_spell):
    index_spell = int(index_spell)
    res = f"\n*{spell_names[index_spell]}*"
    cell = spells_data["cell"][index_spell]
    class_spell = ", ".join(spells_data["class"][index_spell])
    if  cell == "0":
        res += "\n_Заговор_"
    else:
        res += f"\n_{cell} уровень,_" 
    res += f" _{spells_data["school"][index_spell]}_"
    res += "\n_" + class_spell + "_"
    res += f"\n*Время накладывания:* {spells_data["time"][index_spell]}"
    res += f"\n*Дистанция:* {spells_data["distance"][index_spell]}"
    res += f"\n*Компоненты:* {spells_data["components"][index_spell]}"
    res += f"\n*Длительность:* {spells_data["duration"][index_spell]}"
    res += f"\n{spells_data["description"][index_spell]}"
    if pd.notna(spells_data["upgrade"][index_spell]):
        if cell== 0:
            res += f"\n*Улучшение заговора:*"
        else:
            res += f"\n*Использование более высокой ячейки:*"
        res += f"\n{spells_data["upgrade"][index_spell]}"
    return res


#Поиск заклинания по названию
async def res_search(message):
    kb = None
    for index_spell in range(len(spell_names)):
        if message.text.lower() == spell_names[index_spell].lower():
            result = await spell_printer(index_spell)
            favourites_list = await get_favourites_spells_index(message.from_user.id)
            kb = generate_add_del_keyboard(index_spell, favourites_list)
            result = "*Заклинание найденно:*" + result
            break 
    else:
        result = f"*Заклинание* _'{message.text}'_, *не найденно!*"
    return result, kb