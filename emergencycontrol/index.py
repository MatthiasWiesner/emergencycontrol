import os
from flask import (
    render_template,
    send_from_directory)

from emergencycontrol import app, db


@app.route('/')
def index():
    return render_template('index.jinja')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.teardown_request
def remove_db_session(exception=None):
    db.session.remove()


@app.errorhandler(403)
def forbidden_403(exception):
    return render_template('forbidden.jinja'), 403
