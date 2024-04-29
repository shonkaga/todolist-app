import sqlite3
from datetime import date, timedelta
import os
from datetime import datetime, timedelta
import calendar

def init_db():

    # if db exists connect 
    db_exists = os.path.exists('./db/database.db')
    connection = sqlite3.connect('./db/database.db')

    # else populate 
    if not db_exists:
        with open('./db/schema.sql', 'r') as f:
            connection.executescript(f.read())
        connection.commit()
        populate_db()

    connection.close()

def populate_db():
    
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
    tasks = db.execute('SELECT * FROM tasks WHERE status = 0 ORDER BY date IS NULL, date').fetchall()
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

def get_completed_tasks():
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks WHERE status = 1 ORDER BY date DESC').fetchall()
    db.close()
    return tasks

def update_task_details(task_id, name, date):
    db = get_db()
    db.execute('UPDATE tasks SET name = ?, date = ? WHERE id = ?', (name, date, task_id))
    db.commit()
    db.close()

def is_same_week(d1):
    d2 = datetime.today().date()
    return d1.isocalendar()[1] == d2.isocalendar()[1] and d1.year == d2.year    

def update_task_dates(raw_tasks, active_tasks, days_dict):
    for day in calendar.day_name:
        days_dict[day] = []

    for row in raw_tasks:
        task = dict(row)
        if task['date']:
            task_date = datetime.strptime(task['date'], '%Y-%m-%d').date()
            if is_same_week(task_date):
                day_name = calendar.day_name[task_date.weekday()]
                task['date'] = task_date.strftime('%Y-%m-%d')  
                days_dict[day_name].append(task)  
            else:
                task['date'] = task_date.strftime('%Y-%m-%d')
        active_tasks.append(task)


if __name__ == "__main__":
    main()
