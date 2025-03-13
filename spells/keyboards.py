from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from spells.edit_DataBace import *
from spells.df_editor import spell_names, spells_data


#Инлайн кнопки для добавления\удаления спеллов в избранное
def generate_add_del_keyboard(index_spell, favourites_list):
    builder = InlineKeyboardBuilder()
    if favourites_list == None: 
        builder.add(types.InlineKeyboardButton(text="Добавить в избранное", callback_data= str(index_spell) + "_add_spell"))
    elif str(index_spell) in str(favourites_list).split(","):
        builder.add(types.InlineKeyboardButton(text="Удалить из избранного", callback_data= str(index_spell) + "_del_spell"))
    else:
        builder.add(types.InlineKeyboardButton(text="Добавить в избранное", callback_data= str(index_spell) + "_add_spell"))
    return builder.as_markup()


#Обработчик нажатий добавления\удаления спеллов в избранное
async def edit_add_del_keyboard(callback):
    index_spell = callback.data.replace("_spell", "")[:-4]
    favourites_list = await get_favourites_spells_index(callback.from_user.id)

    spell_name = spell_names[int(index_spell)]

    if callback.data.endswith("_add_spell"):
        if favourites_list == None:
            favourites_list = str(index_spell)
        else:    
            favourites_list = str(favourites_list)
            favourites_list += "," + str(index_spell)
        await update_favourites_spells_index(callback.from_user.id, favourites_list)
        text = f"Заклинание {spell_name} добавленно в избранное"

    elif callback.data.endswith("_del_spell"):
        if favourites_list == None:
            new_favourites_list = None
        else:    
            favourites_list = str(favourites_list).split(",")
            if len(favourites_list) == 1:
                new_favourites_list = None
            else:
                favourites_list.remove(str(index_spell))
                new_favourites_list = str(favourites_list[0])
                if len(favourites_list) != 1:
                    for i in favourites_list[1:]:
                        new_favourites_list += "," + str(i)
        await update_favourites_spells_index(callback.from_user.id, new_favourites_list)
        text = f"Заклинание {spell_name} удалено из избранного"
    
    kb = generate_add_del_keyboard(index_spell, favourites_list) 
    return text, kb


#Генератор списка избранных заклинаний
async def generate_favourites_keyboard(message: types.Message):
    favourites_list = await get_favourites_spells_index(message.from_user.id)
    if favourites_list != None:
        favourites_list = str(favourites_list).split(",")
        builder = InlineKeyboardBuilder()
        for index_spell in favourites_list:
            spell_name = str(spell_names[int(index_spell)])
            spell_cell = str(spells_data['cell'][int(index_spell)])
            if spell_cell == "0":
                text = spell_name + "   Заговор"
            else:
                text = spell_name + "   " + spell_cell + " ячейка"
            builder.row(types.InlineKeyboardButton(text=text, callback_data=index_spell + "_spell_seeker"))
        nums_spell = len(favourites_list)
        if nums_spell == 1:
            text = f"В избранном {str(nums_spell)} заклинание."
        elif nums_spell <= 4:
            text = f"В избранном {str(nums_spell)} заклинания."
        else:
            text = f"В избранном {str(nums_spell)} заклинаний."
        kb = builder.as_markup()
        
    else:
        kb = None
        text = "У вас нет избранных заклинаний!"
    return text, kb
        
#Генератор найденных по фильтрам заклинаний и размещение на разных страницах
async def filtered_spell_generator_keyboard(index_spells, page):
    builder = InlineKeyboardBuilder()
    index_spells = index_spells.split(",")
    for index in index_spells[(page*10)-10:(page*10)]:
        if index != "":
            spell_name = str(spell_names[int(index)])
            spell_cell = str(spells_data['cell'][int(index)])
            if spell_cell == "0":
                text = spell_name + "   Заговор"
            else:
                text = spell_name + "   " + spell_cell + " ячейка"
            builder.row(types.InlineKeyboardButton(text=text, callback_data=index + "_spell_seeker"))
    if len(index_spells) - (page*10) > 0:
        builder.row(types.InlineKeyboardButton(text="Далее", callback_data="keyboard_filter_" + str(page + 1)))
    if page != 1:    
        builder.row(types.InlineKeyboardButton(text="Назад", callback_data="keyboard_filter_" + str(page - 1)))

    return builder.as_markup()