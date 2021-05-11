from flask import Flask
from flask_pymongo import PyMongo
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object("config.Config")
mongo = PyMongo(app)
socketio = SocketIO(app)

from .site.views import site
app.register_blueprint(site, url_prefix='/')