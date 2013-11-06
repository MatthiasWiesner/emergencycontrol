import os
import json
from datetime import timedelta

credentials = json.load(open(os.environ['CRED_FILE']))

DB_URI = 'mysql://{user}:{password}@{host}/{dbname}?charset=utf8'.format(
    user=credentials['MYSQLS']['MYSQLS_USERNAME'],
    password=credentials['MYSQLS']['MYSQLS_PASSWORD'],
    host=credentials['MYSQLS']['MYSQLS_HOSTNAME'],
    dbname=credentials['MYSQLS']['MYSQLS_DATABASE'])
DEBUG = True
SECRET_KEY = 'foobarbaz'
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
REMEMBER_COOKIE_DURATION = timedelta(days=30)