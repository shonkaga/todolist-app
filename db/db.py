import sqlite3
from datetime import date, timedelta
import os

def init_db():

    # Check if the database file already exists
    db_exists = os.path.exists('./db/database.db')
    # Connect to the database, ensuring the path is correct
    connection = sqlite3.connect('./db/database.db')

    if not db_exists:
        # Create the tables according to schema.sql if database does not exist
        with open('./db/schema.sql', 'r') as f:
            connection.executescript(f.read())
        connection.commit()
        # Populate the database if it was just created
        populate_db()

    connection.close()

def populate_db():
    # Connect to the database
    connection = sqlite3.connect('./db/database.db')
    cur = connection.cursor()

    # Today and future dates
    today = date.today()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)

    # Insert tasks
    tasks = [
        ('Physics HW', 0, today),
        ('Clean bathroom', 0, today),
        ('Cook dinner', 0, today),
        ('Algorithm HW', 0, tomorrow),
        ('Interview', 0, tomorrow),
        ('Laundry', 0, day_after_tomorrow)
    ]
    cur.executemany("INSERT INTO tasks (name, status, date) VALUES (?, ?, ?)", [(t[0], t[1], t[2].strftime('%Y-%m-%d')) for t in tasks])

    connection.commit()
    connection.close()

def main():
    # Initialize and possibly populate the database
    init_db()


def get_db():
    connection = sqlite3.connect('./db/database.db')
    connection.row_factory = sqlite3.Row
    return connection

def add_task(name, status, date=None):
    db = get_db()
    db.execute('INSERT INTO tasks (name, status, date) VALUES (?, ?, ?)', (name, status, date))
    db.commit()
    db.close()

def get_tasks():
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks ORDER BY date IS NULL, date').fetchall()
    db.close()
    return tasks

def update_task(id, status):
    db = get_db()
    db.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, id))
    db.commit()
    db.close()

def delete_task(id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (id,))
    db.commit()
    db.close()

def get_task(id):
    conn = get_db()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    conn.close()
    return task

if __name__ == "__main__":
    main()
