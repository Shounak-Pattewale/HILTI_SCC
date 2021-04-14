from flask import Blueprint, render_template, redirect, abort
from flask import request, jsonify, make_response, url_for
from datetime import datetime
from flask import session
from flask import flash
import bcrypt
from flask import g
import os
import smtplib

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
    rotate = data['Rotation']
    proc_temp = data['ProcTemp']
    air_temp = data['AirTemp']
    torque = data['Torque']
    
    # vib_list = daily_data(date, time, data)
  
    return render_template("dashboard.html", data=data, vib=vibration, vol=volt, rot=rotate, date=date, time=time)


@site.route("/user_profile")
def user_profile():
    return render_template("user_profile.html")
