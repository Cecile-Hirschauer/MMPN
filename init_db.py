import sqlite3
from hashlib import md5

DATABASE = 'app.db'
db = sqlite3.connect(DATABASE)

cursor = db.cursor()

# Creation of table "categories".
# If it existed already, we delete the table and create a new one
cursor.execute('DROP TABLE IF EXISTS categories')
cursor.execute("""CREATE TABLE categories
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL)""")

# We seed the table with initial values.
# Here we insert 3 categories: "Videogames", "Boardgames" and "Outdoors"
for name in ["Videogames", "Boardgames", "Outdoor"]:
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))

# Creation of table "toys"
cursor.execute("DROP TABLE IF EXISTS toys")
cursor.execute("""CREATE TABLE toys
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                description VARCHAR(200) NOT NULL,
                price INTEGER NOT NULL,
                category_id INTEGER,
                CONSTRAINT fk_categories
                FOREIGN KEY (category_id)
                REFERENCES categories(category_id))""")

# We seed the table with initial values.
# Here 5 toys are inserted into the table "toys"
for data in [
    ("Playstation 4", "Famous video game platform", 499, 1),
    ("Barbie", "Pink doll", 29, None),
    ("Monopoly", "Board game $$$", 59, 2),
    ("Football ball", "A ball to play outside", 25, 3),
    ("Chess", "Board game for smart children", 25, 2),
]:
    if data[-1] is None:
        cursor.execute(
            "INSERT INTO toys (name, description, price) VALUES (?, ?, ?)",
            data[0:3])
    else:
        cursor.execute(
            """INSERT INTO toys (name, description, price, category_id)
            VALUES (?, ?, ?, ?)""",
            data)

# Creation of table "elves"
cursor.execute("DROP TABLE IF EXISTS elves")
cursor.execute("""CREATE TABLE elves (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   first_name VARCHAR(200) NOT NULL,
                                   last_name VARCHAR(200) NOT NULL,
                                   login VARCHAR(200) NOT NULL,
                                   password VARCHAR(200) NOT NULL UNIQUE)
                                   """)


# I seed the table with initial values.
# Here 4 elves are inserted into the table "elves"
# psd md5 => secret = 5ebe2294ecd0e0f08eab7690d2a6ee69
#     => christmas = 3d4fe7a00bc6fb52a91685d038733d6f
#     => girafe = b4c4bfec4e7ff1d0a7ceb40d1ec56292
#     => banane = 5473e3f141e0328ce87dac9366e0aace

# for elf in [
#     ("Bushy", "Evergreen", "Bgreen", '5ebe2294ecd0e0f08eab7690d2a6ee69'),
#     ("Shinny", "Upatree", "Satree", '3d4fe7a00bc6fb52a91685d038733d6f'),
#     ("Pepper", "Minstix",'Pnstix' , 'b4c4bfec4e7ff1d0a7ceb40d1ec56292')
# ]:
#     cursor.execute(
#         """
#         INSERT INTO elves
#         (first_name, last_name, login, password)
#         VALUES (?, ?, ?, ?)
#         """,
#         elf
#     )

# wishes table
cursor.execute("DROP TABLE IF EXISTS wishes")
cursor.execute(
    """ CREATE TABLE wishes (id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_name VARCHAR(255) NOT NULL,
    toy_id INTEGER NOT NULL,
    CONSTRAINT fk_toys
    FOREIGN KEY (toy_id)
    REFERENCES toys(toy_id))"""
)
 
# schedules table
cursor.execute('DROP TABLE IF EXISTS schedules')
cursor.execute(
    """ CREATE TABLE schedules
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     elf_id INTEGER NOT NULL,
     wish_id INTEGER NOT NULL,
     done BOOlEAN NOT NULL DEFAULT False,
     done_at DATE DEFAULT None,
     CONSTRAINT fk_elves
     FOREIGN KEY (elf_id)
     REFERENCES elves(elf_id),
     CONSTRAINT fk_wishes
     FOREIGN KEY (wish_id)
     REFERENCES  wishes(wish_id)
    )
    """
)
# We save our changes into the database file
db.commit()

# We close the connection to the database
db.close()
