import os
import config
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from apps.controllers import api

app.register_blueprint(api, url_prefix='')