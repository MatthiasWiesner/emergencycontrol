import json
import urllib2
from emergencycontrol import app
from flask_login import login_required
from flask import render_template


def fetch_data():
    content = urllib2.urlopen("https://kpi.cloudcontrolled.com/kpi/tasks").read()
    data = json.loads(content)
    task_open = None
    task_executed = None
    for task_data in data['series']:
        if task_data['name'] == 'task_open':
            task_open = task_data['data']
        if task_data['name'] == 'task_executed':
            task_executed = task_data['data']
    return task_open, task_executed


@app.route('/showtasks')
@login_required
def showtasks():
    task_open, task_executed = fetch_data()
    return render_template('tasks.jinja', task_open=json.dumps(task_open), task_executed=json.dumps(task_executed))


@app.route('/tasks')
@login_required
def tasks():
    task_open, task_executed = fetch_data()
    return json.dumps({
        'taskOpen': task_open,
        'taskExecuted': task_executed
    })
