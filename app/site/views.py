from flask import Blueprint, render_template, redirect, abort
from flask import request, jsonify, make_response, url_for
from datetime import datetime
from flask import session
from flask import flash
import bcrypt
from time import time
import random
import json

site = Blueprint("site", __name__, template_folder='../templates', static_folder='static',static_url_path='static')

# Custom imports
from app import *
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

# def daily_data(data):
#     # Date formate -> MM-DD=YYYY
#     vibration_list = []
#     vibrate = 0
#     print("okay")
#     for i in data.index:
#         date = data['date'][i]
#         while date == '01-01-2015':
#             # vibrate += data['vibration'][i]
#             vibration_list.append(data['vibration'][i])
#             break
#         else:
#             print('Done')
    
#     return vibration_list


@site.route("/dashboard")
def dashboard():
    data = tool.data()
    rotate = data['Rpm']
    proc_temp = data['Process temp']
    toolwear = data['Tool wear']
    torque = data['Torque']
    x = data['date']
    # rotate_list = daily_data(date, time, data)
  
    return render_template("dashboard.html", data=data, rotate=rotate, proc_temp=proc_temp, toolwear=toolwear, torque=torque, x=x)


@site.route('/data', methods=["GET", "POST"])
def data():
    data = [time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@site.route("/user_profile")
def user_profile():
    return render_template("user_profile.html")
