from flask import Blueprint, render_template, redirect, abort, session
from flask import request, jsonify, make_response, url_for, flash
from datetime import datetime
import bcrypt
from time import time
import random
import json
from flask_socketio import send
import pickle

site = Blueprint("site", __name__, template_folder='../templates', static_folder='static',static_url_path='static')

model = pickle.load(open('/mnt/d/Taha/HILTI_SCC/app/site_data/trained.pkl', 'rb'))
# model = pickle.load(open('/mnt/d/Shounak/My Projects/HILTI_SCC/app/site_data/trained.pkl', 'rb'))

# Custom imports
from app import *
# from app import socketio
# from app import df

from .models import *
tool = Tools()


@site.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    return (resp, 200)

@site.route("/")
def index():
    # tool.data()
    return render_template("home.html")

def prediction(x):
    pred = model.predict([x])
    print('Prediction : ',pred[0])

@site.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')
    # data = tool.data()
    # rotate = data['Rpm']
    # proc_temp = data['Process temp']
    # toolwear = data['Tool wear']
    # torque = data['Torque']
    # x = data['date']
  
    # return render_template("dashboard.html", data=data, rotate=rotate, proc_temp=proc_temp, toolwear=toolwear, torque=torque, x=x)

@socketio.on('message')
def handle_message(resp):
    print('Message: ', resp)
    prediction(resp)
    

@site.route("/user_profile")
def user_profile():
    return render_template("user_profile.html")
