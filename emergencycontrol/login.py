from json import loads
import requests
from flask import (
    session,
    request,
    redirect,
    url_for,
    flash)
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required)
from flask_login import LoginManager
from flask_oauth import OAuth

from emergencycontrol import app, db
from .model import Person


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


google = OAuth().remote_app(
    'google',
    base_url='https://www.google.com/accounts/',
    authorize_url=app.config.get('GOOGLE_API_AUTH_URI'),
    request_token_url=None,
    request_token_params= {
        'scope':
            'https://www.googleapis.com/auth/userinfo.email \
             https://www.googleapis.com/auth/userinfo.profile',
        'response_type': 'code'},
    access_token_url=app.config.get('GOOGLE_API_TOKEN_URI'),
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=app.config.get('GOOGLE_API_CLIENT_ID'),
    consumer_secret=app.config.get('GOOGLE_API_CLIENT_SECRET'))


@login_manager.user_loader
def load_user(person_id):
    return Person.load(person_id)


@app.route('/login')
def login():
    session['next'] = request.args.get('next') or request.referrer or None
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    callback=url_for('google_callback', _external=True, _scheme='https')
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
                db.session.add(person)
                db.session.commit()
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
