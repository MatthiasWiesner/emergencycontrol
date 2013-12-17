import os
import json
from datetime import timedelta

_credentials = None
if not _credentials:
    _credentials = json.load(open(os.environ['CRED_FILE']))
    for k in _credentials['CONFIG']['CONFIG_VARS']:
        vars()[k.upper()] = _credentials['CONFIG']['CONFIG_VARS'][k]

SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}/{dbname}?charset=utf8'.format(
    user=_credentials['MYSQLS']['MYSQLS_USERNAME'],
    password=_credentials['MYSQLS']['MYSQLS_PASSWORD'],
    host=_credentials['MYSQLS']['MYSQLS_HOSTNAME'],
    dbname=_credentials['MYSQLS']['MYSQLS_DATABASE'])

DEBUG = bool(os.getenv('DEBUG'))
SECRET_KEY = 'foobarbaz'
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
REMEMBER_COOKIE_DURATION = timedelta(days=30)
