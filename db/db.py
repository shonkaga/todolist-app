import sqlite3

def init_db():
    connection = sqlite3.connect('./db/database.db')

    with open('./db/schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    cur.execute("INSERT INTO tasks (name, status, date) VALUES (?, ?, ?)",
                ('447 HomeWork', 0, '2024-4-10')
                )

    cur.execute("INSERT INTO tasks (name, status, date) VALUES (?, ?, ?)",
                ('447 Group Meeting', 0, '2024-4-12')
                )

    cur.execute("INSERT INTO tasks (name, status, date) VALUES (?, ?, ?)",
                ('Learn how to code', 1, None)
                )

    cur.execute("INSERT INTO tasks (name, status, date) VALUES (?, ?, ?)",
                ('Make a website', 0, None)
                )

    connection.commit()
    connection.close()
