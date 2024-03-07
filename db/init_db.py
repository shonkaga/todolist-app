import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO tasks (name, status) VALUES (?, ?)",
            ('447 HomeWork', 0)
            )

cur.execute("INSERT INTO tasks (name, status) VALUES (?, ?)",
            ('447 Group Meeting', 0)
            )

cur.execute("INSERT INTO tasks (name, status) VALUES (?, ?)",
            ('Learn how to code', 1)
            )

cur.execute("INSERT INTO tasks (name, status) VALUES (?, ?)",
            ('Make a website', 0)
            )

connection.commit()
connection.close()