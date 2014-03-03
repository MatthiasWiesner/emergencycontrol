import json
import urllib2
from emergencycontrol import app
from flask_login import login_required
from flask import render_template


@app.route('/showtasks')
@login_required
def showtasks():
    return render_template('tasks.jinja')


@app.route('/tasks')
#@login_required
def tasks():
    return urllib2.urlopen("https://kpi.cloudcontrolled.com/kpi/tasks").read()
