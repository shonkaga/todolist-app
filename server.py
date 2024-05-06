

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField
from wtforms.validators import DataRequired, Optional
from flask_wtf.csrf import CSRFProtect

# db functions 
from db import get_tasks, add_task, update_task, get_task, delete_task, init_db, get_completed_tasks, update_task_details, is_same_week, update_task_dates, pull_events, push_events, check_creds, get_tomorrow_schedule




init_db()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
csrf = CSRFProtect(app)

class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    status = BooleanField('Status')
    date = DateField('Date', format='%Y-%m-%d', validators=[Optional()])
    submit = StringField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        add_task(form.name.data, form.status.data, form.date.data)
        return redirect(url_for('index'))
    
    raw_tasks = get_tasks() 
    active_tasks = []
    days_dict = {}
    update_task_dates(raw_tasks,active_tasks,days_dict)
    next_tasks = get_tomorrow_schedule()
    
    completed_tasks = get_completed_tasks()  
    return render_template('index.html', active_tasks=active_tasks, completed_tasks=completed_tasks, form=form, days_dict=days_dict, next_tasks=next_tasks)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = get_task(id)
    if task is None:
        return "Task not found", 404

    form = TaskForm(obj=task) 
    if request.method == 'POST' and form.validate_on_submit():
        update_task_details(id, form.name.data, form.date.data)
        return redirect(url_for('index'))
    
    return render_template('edit_task.html', form=form, task_id=id)



@app.route('/complete_task/<int:id>', methods=['POST'])
def complete_task(id):
    update_task(id, 1)  # 1 represents a completed task
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_task(id) 
    return redirect(url_for('index'))

@app.route('/pull_events', methods=['POST'])
def pull():
    pull_events()
    return redirect(url_for('index'))

@app.route('/push_events', methods=['POST'])
def push():
    push_events()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
