import os
from json import loads
import requests
from flask import (
    Flask,
    session,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required)
from flask_oauth import OAuth
from flask_sslify import SSLify

from .model import Person, init_engine, db_session

from . import config
app = Flask(__name__)
app.debug = config.DEBUG
app.config.from_object(config)
SSLify(app, subdomains=True)

init_engine(app.config['DB_URI'])

oauth = OAuth()
google = oauth.remote_app(
    'google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params= {
        'scope':
            'https://www.googleapis.com/auth/userinfo.email \
             https://www.googleapis.com/auth/userinfo.profile',
        'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key='747740959147-a1oj10ealq6q58gebu89uthqanpq2dl7.apps.googleusercontent.com',
    consumer_secret='CdNLY5AK5ZCl-UCs_5DWQcFd')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# needs the LoginManager to reload a person
@login_manager.user_loader
def load_user(person_id):
    return Person.load(person_id)


from . import calendar
from . import person
from . import alerts


@app.route('/')
def index():
    return render_template('index.jinja')


@app.route('/login')
def login():
    session['next'] = request.args.get('next') or request.referrer or None
    callback=url_for('google_callback', _external=True)
    return google.authorize(callback=callback)


@app.route('/google_callback')
@google.authorized_handler
def google_callback(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    if access_token:
        r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
            headers={'Authorization': 'OAuth ' + access_token})
        if r.ok:
            google_profile = loads(r.text)
            if not 'hd' in google_profile or google_profile['hd'] != 'cloudcontrol.de':
                flash("You are not from cloudControl", 'error')
                return redirect(url_for('index'))
            person = Person.query.filter_by(google_id=google_profile['id']).first()
            if person is None:
                keys = ['phone', 'picture', 'link', 'name','hd', 'email']
                data = dict([(k,google_profile[k]) for k in keys if k in google_profile])
                data['google_id'] = google_profile['id']

                person = Person(**data)
                db_session.add(person)
                db_session.commit()
            if login_user(person):
                flash('Logged in successfully!', 'success')
                return redirect(request.args.get('next') or url_for('index'))
            else:
                flash('This person is disabled!', 'error')
        else:
            flash('Invalid google response!', 'error')

    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!')
    return redirect(url_for('index'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.teardown_request
def remove_db_session(exception=None):
    db_session.remove()


@app.errorhandler(403)
def forbidden_403(exception):
    return render_template('forbidden.jinja'), 403
