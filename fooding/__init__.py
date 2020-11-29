from flask import Flask

from fooding.config import Config
from fooding.models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

from fooding.views import *
