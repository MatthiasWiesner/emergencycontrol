from flask import Flask
from flask_sslify import SSLify
from flask_sqlalchemy import SQLAlchemy

from . import config

app = Flask(__name__)
app.debug = config.DEBUG
app.config.from_object(config)

SSLify(app, subdomains=True)

db = SQLAlchemy(app)

from . import index
from . import login
from . import calendar
from . import person
from . import alerts
