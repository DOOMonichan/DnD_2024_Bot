import pandas as pd

#Блок кода переводит все кроме описания заклинаний к нижнему регистру и строковый тип данных
spells_data = pd.read_csv("spells\spells_phb_2024.csv")
spell_names = spells_data['name'].tolist()
spells_data["cell"] = spells_data["cell"].astype(str)
spells_data["class"] = spells_data["class"].apply(lambda x: x.lower().split(", "))
spells_data["school"] = spells_data["school"].apply(lambda x: x.lower())
spells_data["time_filter"] = spells_data["time_filter"].apply(lambda x: x.lower().split(", "))
spells_data["distance_filter"] = spells_data["distance_filter"].apply(lambda x: x.lower())
spells_data["components_filter"] = spells_data["components_filter"].apply(lambda x: x.lower().split(", "))
spells_data["duration_filter"] = spells_data["duration_filter"].apply(lambda x: x.lower())

#Функция для создание маски на DF
def isin_list(spell_value, list_filter):
    for i in list_filter:
      if i in spell_value:
         return True
    else:
       return False


#Применение фильтров к DF
async def applying_filters(dict_filter):
    dict_filter["cells"] = ",".join(dict_filter["cells"]).replace("Заговор", "0").split(",")
    for k, v in dict_filter.items():
       dict_filter[k] = [v.lower() for v in dict_filter[k]]

    cells = spells_data["cell"].isin(dict_filter["cells"])
    classes = spells_data["class"].apply(lambda spell_value: isin_list(spell_value, dict_filter["class"]))
    school = spells_data["school"].isin(dict_filter["school"])
    time = spells_data["time_filter"].apply(lambda spell_value: isin_list(spell_value, dict_filter["time"]))
    distance = spells_data["distance_filter"].isin(dict_filter["distance"])
    if dict_filter["components"] == ["вербальный", "соматический", 
                                     "материальный не расходуемый", "материальный расходуемый"]:
        components = True
    else:  
        components = spells_data["components_filter"].apply(lambda value: value == dict_filter["components"])
    duration = spells_data["duration_filter"].isin(dict_filter["duration"])
    
    df_filter = spells_data[cells & classes & school & time & distance & components & duration]
    return df_filter
