from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object("config.Config")
mongo = PyMongo(app)

from .site.views import site
app.register_blueprint(site, url_prefix='/')