from flask import Flask, render_template, jsonify
import sqlite3
from db.db import init_db

# create flask app 
app = Flask(__name__)

# start the db 
init_db()

def get_tasks():
    conn = sqlite3.connect('db/database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks

# Route to display tasks
@app.route('/')
def show_tasks():
    tasks = get_tasks()


if __name__ == '__main__':
    app.run(debug=True)

