from sqlite3 import connect


def sql_con():
    with connect(
            database="data.db",
            check_same_thread=False) as con:
        cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER,
        first_name TEXT,
        last_name TEXT,
        theme TEXT,
        color TEXT)""")


def existing_checker(user_id):
    with connect(database='data.db') as con:
        cur = con.cursor()

    cur.execute("SELECT user_id FROM users WHERE user_id = (?)", (user_id,))
    con.commit()

    if cur.fetchone() is None:
        return False
    else:
        return True


def new_user(user_id, first_name, last_name):
    with connect(database='data.db') as con:
        cur = con.cursor()

    query = """INSERT INTO users(user_id, first_name, last_name) VALUES(?,?,?)"""

    cur.execute(query, (user_id, first_name, last_name,))
    con.commit()


def updater_theme(user_id, theme):
    with connect(database='data.db') as con:
        cur = con.cursor()

    cur.execute(
        "UPDATE users SET theme = (?) WHERE user_id = (?)",
        (theme, user_id,)
    )
    con.commit()


def updater_color(user_id, color):
    with connect(database='data.db') as con:
        cur = con.cursor()

    cur.execute(
        "UPDATE users SET color = (?) WHERE user_id = (?)",
        (color, user_id,)
    )
    con.commit()


def themeANDcolor(user_id):
    with connect(database='data.db') as con:
        cur = con.cursor()

    cur.execute("SELECT theme FROM users WHERE user_id = (?)", (user_id,))
    theme = cur.fetchone()[0]
    cur.execute("SELECT color FROM users WHERE user_id = (?)", (user_id,))
    color = cur.fetchone()[0]

    # print({"theme": theme, "color": color})

    return {"theme": theme, "color": color}
