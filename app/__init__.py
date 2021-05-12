from flask import Flask
from flask_pymongo import PyMongo
from flask_socketio import SocketIO

# Google oAuth api
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config.from_object("config.Config")
mongo = PyMongo(app)
socketio = SocketIO(app)
oauth = OAuth(app)

from .site.views import site
app.register_blueprint(site, url_prefix='/')