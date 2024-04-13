from datetime import datetime, timedelta
import calendar
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField
from wtforms.validators import DataRequired, Optional

# Importing your db module (ensure all necessary functions are defined)
from db import get_tasks, add_task, update_task, get_task, delete_task, init_db

def is_same_week(d1):
    d2 = datetime.today().date()
    # Checks if two dates are in the same week considering Monday as the first day of the week
    return d1.isocalendar()[1] == d2.isocalendar()[1] and d1.year == d2.year    



init_db()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    status = BooleanField('Status')
    date = DateField('Date', format='%Y-%m-%d', validators=[Optional()])
    submit = StringField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        # Using add_task from db.py to add a new task
        add_task(form.name.data, form.status.data, form.date.data)
        return redirect(url_for('index'))
    
    raw_tasks = get_tasks()  # Getting all tasks using get_tasks from db.py
    tasks = []
    today = datetime.today().date()

    for row in raw_tasks:
        task = dict(row)  # Convert sqlite3.Row to a dictionary
        if task['date']:
            task_date = datetime.strptime(task['date'], '%Y-%m-%d').date()
            if (is_same_week(task_date)):
                # If the task is within the next week and on a future day of the current week
                task['date'] = calendar.day_name[task_date.weekday()]  # Shows day of the week
            else:
                task['date'] = task_date.strftime('%Y-%m-%d')  # Shows full date
        tasks.append(task)
    
    return render_template('index.html', tasks=tasks, form=form)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = get_task(id)  # Assuming you have or will add a get_task function in db.py
    if task is None:
        return redirect(url_for('index'))

    form = TaskForm()
    if request.method == 'GET':
        form.name.data = task['name']
        form.status.data = bool(task['status'])
        form.date.data = task['date']

    if form.validate_on_submit():
        # Using update_task from db.py to update an existing task
        update_task(id, form.status.data)
        return redirect(url_for('index'))
    
    return render_template('edit.html', form=form, task_id=id)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_task(id)  # Using delete_task from db.py to delete a task
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
