import locale

from flask import Flask

from fooding.config import Config
from fooding.models import db, migrate

locale.setlocale(locale.LC_ALL, '')
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

from fooding.views import *
