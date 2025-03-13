import aiosqlite
import sys
import pathlib

script_dir = pathlib.Path(sys.argv[0]).parent
DB_FAVOURITES = script_dir /"spells"/'favourites.db'
DB_FILTER = script_dir /"spells"/'filter.db'

#Создание и обработка БД избранных заклинаний для каждого пользователя
async def update_favourites_spells_index(user_id, index_spells):
    async with aiosqlite.connect(DB_FAVOURITES) as db:
        await db.execute('UPDATE favourites_spells SET (spell_index_favorite) = (?) WHERE user_id = ?', (index_spells, user_id))
        await db.commit()


async def get_favourites_spells_index(user_id):
     async with aiosqlite.connect(DB_FAVOURITES) as db:
        async with db.execute('SELECT spell_index_favorite FROM favourites_spells WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return None
            

async def rec_new_user(user_id, username):
    async with aiosqlite.connect(DB_FAVOURITES) as db:
        await db.execute('INSERT OR REPLACE INTO favourites_spells (user_id, username, spell_index_favorite) VALUES (?, ?, ?)', (user_id, username, None))
        await db.commit()


async def create_table_favourites_spells():
    async with aiosqlite.connect(DB_FAVOURITES) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS favourites_spells (user_id INTEGER PRIMARY KEY, username TEXT NOT NULL, spell_index_favorite TEXT)''')
        await db.commit()


#Создание и обработка БД фильтров для каждого пользователя
async def update_filter_param(user_id, param, value_param):
    async with aiosqlite.connect(DB_FILTER) as db:
        await db.execute(f'UPDATE filter_spells SET ({param}) = (?) WHERE user_id = ?', (value_param, user_id))
        await db.commit()


async def get_filter_param(user_id, param):
     async with aiosqlite.connect(DB_FILTER) as db:
        async with db.execute(f'SELECT {param} FROM filter_spells WHERE user_id = (?)', (user_id, )) as cursor:
            result = await cursor.fetchone()
            return result[0]


async def rec_new_filter(user_id):
    async with aiosqlite.connect(DB_FILTER) as db:
        await db.execute('INSERT OR REPLACE INTO filter_spells (user_id, cells, school, class, time, distance, components, duration, index_list, tabs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, "0000000000", "00000000", "00000000", "000000", "0000000", "0000", "0000000", "", "0000000"))
        await db.commit()


async def create_table_filter_spells():
    async with aiosqlite.connect(DB_FILTER) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS filter_spells (user_id INTEGER PRIMARY KEY, cells TEXT, school TEXT, class TEXT, time TEXT, distance TEXT, components TEXT, duration TEXT, index_list TEXT, tabs TEXT)''')
        await db.commit()      